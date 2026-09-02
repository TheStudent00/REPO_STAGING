"""Acceptance gate for the C++ ingress transpiler (Phase 2 of the plan).

Cranelift's Rust encoder and LLVM's C++ encoder are two independent
implementations of the SAME x86-64 ISA facts. This file checks that the
LLVM-derived Python (llvm_encoder_gen.py, transpiled by transpile_cpp.py
from X86MCCodeEmitter.cpp) agrees EXHAUSTIVELY with the Cranelift-derived
Python we already trust (../vocab_transpiler/vocab_support.py, itself
verified byte-identical against native rustc -- see
../vocab_transpiler/README.md). Two independent compilers, two
independent transpilers, one answer: diverse-double-compiling applied to
our own pipeline.

Three checks, each stated in the plan:
  1. modRMByte(Mod, RegOpcode, RM)      vs encode_modrm(m0d, enc_reg_g, rm_e)
     -- all 256 combinations in the asserted domain (Mod<4, RegOpcode<8,
     RM<8), PLUS a report on what happens OUTSIDE that domain.
  2. REX byte  -- LLVM's 0x40|W<<3|R<<2|X<<1|B (via setR/setB/setW) vs
     Cranelift's RexPrefix.mem_op/two_op -- exhaustive over all 8-bit
     register encodings x W in {0,1}.
  3. SIB byte  -- emitSIBByte (== modRMByte under a different field
     naming) vs Cranelift's encode_sib -- all 256 combinations in the
     asserted domain (SS<4, Index<8, Base<8).
"""

import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "vocab_transpiler"))

import llvm_encoder_gen as llvm
from vocab_support import encode_modrm, encode_sib, RexPrefix

ok = True


def report(label, passed, detail=""):
    global ok
    ok = ok and passed
    print(f"{'PASS' if passed else 'FAIL'}  {label}"
          + (f"  {detail}" if detail else ""))


# =================================================================
# 1. modRMByte vs encode_modrm -- exhaustive over the asserted domain
# =================================================================

print("--- (1) modRMByte vs encode_modrm ---")
n_checked = 0
n_mismatch = 0
mismatches = []
for mod_ in range(4):
    for reg_opcode in range(8):
        for rm in range(8):
            llvm_byte = llvm.mod_rm_byte(mod_, reg_opcode, rm)
            cranelift_byte = encode_modrm(mod_, reg_opcode, rm)
            n_checked += 1
            if llvm_byte != cranelift_byte:
                n_mismatch += 1
                mismatches.append((mod_, reg_opcode, rm, llvm_byte, cranelift_byte))

report("modRMByte == encode_modrm over all 256 in-domain combinations",
       n_mismatch == 0,
       f"checked={n_checked} mismatches={n_mismatch}")
for m in mismatches[:8]:
    print("     mismatch:", m)

# ---- outside the asserted domain: a real, measured finding, not a guess.
#
# Both modRMByte (C++ `assert(...)`) and encode_modrm (Rust
# `debug_assert!(...)`, transpiled 1:1 in vocab_support.py) refuse
# out-of-domain input the same way *in this Python transpile*, because
# Python's `assert` is on by default in both files -- so calling either
# guarded function outside its domain raises AssertionError in both,
# which would look like "they agree" while hiding the real difference.
#
# The real difference is in what each COMPILED LANGUAGE does in its
# normal shipping configuration:
#   - Rust's debug_assert! is unconditionally compiled OUT in `--release`
#     builds (Cranelift's normal shipping mode) -- so encode_modrm's
#     masks (`& 3`, `& 7`) are what actually executes in production:
#     out-of-range input is silently wrapped into range.
#   - C++'s assert() is compiled out only when NDEBUG is defined, which
#     LLVM's Release configuration does define -- so modRMByte's raw,
#     UNMASKED arithmetic (`RM | (RegOpcode << 3) | (Mod << 6)`) is what
#     actually executes in production: out-of-range input is NOT wrapped,
#     and can overflow a single byte's worth of bits entirely.
#
# So this test bypasses each guard explicitly and compares the two CORE
# formulas directly, to show the real (measured, not assumed) divergence
# that exists once both guards are compiled away as they are in each
# project's normal release build.
print("\n--- (1b) outside the asserted domain (guards bypassed, as in each "
      "language's release build) ---")


def llvm_core_unmasked(mod_, reg_opcode, rm):
    """The literal modRMByte return expression with its guarding
    assert() removed -- what runs when NDEBUG is defined."""
    return rm | (reg_opcode << 3) | (mod_ << 6)


def cranelift_core_masked(mod_, reg_opcode, rm):
    """The literal encode_modrm return expression with its guarding
    debug_assert! removed -- what runs in a Rust --release build."""
    return ((mod_ & 3) << 6) | ((reg_opcode & 7) << 3) | (rm & 7)


out_of_domain_samples = [
    (4, 0, 0), (0, 8, 0), (0, 0, 8), (7, 15, 15), (255, 255, 255),
]
diverged = 0
for mod_, reg_opcode, rm in out_of_domain_samples:
    a = llvm_core_unmasked(mod_, reg_opcode, rm)
    b = cranelift_core_masked(mod_, reg_opcode, rm)
    same = (a & 0xFF) == b if a <= 0xFF else False
    if a != b:
        diverged += 1
    print(f"  Mod={mod_:>3} RegOpcode={reg_opcode:>3} RM={rm:>3}  "
          f"llvm(unmasked)={a:#06x}  cranelift(masked)={b:#04x}  "
          f"{'DIVERGE' if a != b else 'match'}")
print(f"  finding: {diverged}/{len(out_of_domain_samples)} sampled "
      "out-of-domain inputs diverge once both guards are bypassed -- "
      "LLVM's raw formula can exceed a byte (no masking exists at all in "
      "the source); Cranelift's masks make it wrap silently instead. "
      "This is a real difference between the two source languages' "
      "release-mode behavior, not a transpiler artifact: both this "
      "transpile and vocab_support.py reproduce their source's guard "
      "faithfully (assert vs debug_assert!), and BOTH guards happen to "
      "be Python `assert` today, which is why the guarded functions "
      "above look identical in-domain and both raise the same way "
      "out-of-domain -- only inspecting the core arithmetic directly "
      "(as done here) reveals the divergence.")


# =================================================================
# 2. REX byte -- exhaustive over all 8-bit register encodings x W
# =================================================================

print("\n--- (2) REX byte: X86OpcodePrefixHelper.emit() vs RexPrefix.mem_op/two_op ---")


def llvm_rex_byte(enc_reg, enc_rm, w):
    helper = llvm.X86OpcodePrefixHelper()
    helper.setR(enc_reg)
    helper.setB(enc_rm)
    helper.setW(w)
    helper.Kind = llvm.PK_REX
    cb = []
    helper.emit(cb)
    assert len(cb) == 1, f"emit() produced {len(cb)} bytes, expected 1"
    return cb[0]


n_checked = n_mismatch = 0
mismatches = []
for enc_reg in range(256):
    for w in (0, 1):
        for enc_rm in range(256):
            llvm_byte = llvm_rex_byte(enc_reg, enc_rm, w)
            mem_op_byte = RexPrefix.mem_op(enc_reg, enc_rm, bool(w), False).byte
            two_op_byte = RexPrefix.two_op(enc_reg, enc_rm, bool(w), False).byte
            n_checked += 1
            if llvm_byte != mem_op_byte or llvm_byte != two_op_byte:
                n_mismatch += 1
                mismatches.append((enc_reg, enc_rm, w, llvm_byte, mem_op_byte, two_op_byte))

report("REX byte agrees over all 256*256*2 register-encoding x W combinations",
       n_mismatch == 0,
       f"checked={n_checked} mismatches={n_mismatch}")
for m in mismatches[:8]:
    print("     mismatch (enc_reg, enc_rm, w, llvm, mem_op, two_op):", m)


# =================================================================
# 3. SIB byte -- exhaustive over the asserted domain
# =================================================================

print("\n--- (3) SIB byte: emit_sib_byte/modRMByte vs encode_sib ---")


def llvm_sib_byte(ss, index, base):
    cb = []
    llvm.emit_sib_byte(ss, index, base, cb)
    assert len(cb) == 1
    return cb[0]


n_checked = n_mismatch = 0
mismatches = []
for ss in range(4):
    for index in range(8):
        for base in range(8):
            llvm_byte = llvm_sib_byte(ss, index, base)
            cranelift_byte = encode_sib(ss, index, base)
            n_checked += 1
            if llvm_byte != cranelift_byte:
                n_mismatch += 1
                mismatches.append((ss, index, base, llvm_byte, cranelift_byte))

report("SIB byte agrees over all 256 in-domain (SS<4, Index<8, Base<8) combinations",
       n_mismatch == 0,
       f"checked={n_checked} mismatches={n_mismatch}")
for m in mismatches[:8]:
    print("     mismatch:", m)


# =================================================================
# 4. cut-arm reachability invariant: confirm the cuts actually raise
#    (a cut that silently no-ops instead of raising would be worse than
#    no cut at all -- this is the "asserted, not assumed" check).
# =================================================================

print("\n--- (4) cut arms raise loudly (VEX2/VEX3/XOP/REX2/EVEX) ---")
cut_ok = True
for kind_name in ("REX2", "VEX2", "VEX3", "XOP", "EVEX"):
    helper = llvm.X86OpcodePrefixHelper()
    helper.Kind = llvm.PREFIX_KIND_NAMES[kind_name]
    try:
        helper.emit([])
        print(f"  FAIL  PrefixKind.{kind_name} did not raise -- cut invariant violated")
        cut_ok = False
    except NotImplementedError:
        print(f"  ok    PrefixKind.{kind_name} raises NotImplementedError as required")
ok = ok and cut_ok


print("\nC++ INGRESS ACCEPTANCE:", "ALL PASS" if ok else "FAILURES PRESENT")
raise SystemExit(0 if ok else 1)
