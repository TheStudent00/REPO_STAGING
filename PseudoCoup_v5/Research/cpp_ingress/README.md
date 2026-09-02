# C++ Ingress Transpiler (Phase 2)

Mechanically transpiles a named slice of LLVM's **hand-written** x86
encoder (`X86MCCodeEmitter.cpp`, LLVM `llvmorg-21.1.8`) into Python, and
checks it exhaustively against the Cranelift-derived Python we already
trust (`../vocab_transpiler/vocab_support.py`, itself verified
byte-identical against native `rustc`).

Two independent compilers (LLVM, Cranelift), two independent transpile
pipelines, computing the same x86-64 ISA facts. Agreement here is
diverse-double-compiling applied to our own tooling — see
`DevComms/plan_2026-07-25.md`, Phase 2.

## Result

```
input     X86MCCodeEmitter.cpp (2,034 lines; slice transpiled: ~30 lines)
output    llvm_encoder_gen.py (139 lines)
faults    0 unsupported nodes in the transpiled slice
determinism  regenerate -> byte-identical (no timestamps in output)
```

## Regenerate

```
python3 transpile_cpp.py <path>/X86MCCodeEmitter.cpp [outfile]
```

Defaults to `llvm_encoder_gen.py`. The emitted module carries
provenance: source filename, source sha256, LLVM tag, transpiler
version. No timestamps, so regeneration is deterministic.

## Acceptance

```
python3 test_agreement.py
```

```
--- (1) modRMByte vs encode_modrm ---
PASS  modRMByte == encode_modrm over all 256 in-domain combinations  checked=256 mismatches=0

--- (2) REX byte: X86OpcodePrefixHelper.emit() vs RexPrefix.mem_op/two_op ---
PASS  REX byte agrees over all 256*256*2 register-encoding x W combinations  checked=131072 mismatches=0

--- (3) SIB byte: emit_sib_byte/modRMByte vs encode_sib ---
PASS  SIB byte agrees over all 256 in-domain (SS<4, Index<8, Base<8) combinations  checked=256 mismatches=0

--- (4) cut arms raise loudly (VEX2/VEX3/XOP/REX2/EVEX) ---
  ok    PrefixKind.REX2/VEX2/VEX3/XOP/EVEX all raise NotImplementedError

C++ INGRESS ACCEPTANCE: ALL PASS
```

All three ISA-fact checks pass exhaustively over the asserted / declared
domain (131,072 REX combinations is the largest — every 8-bit register
encoding pair x W ∈ {0,1}). See "Outside the asserted domain" below for
the one genuine finding the test also surfaces.

## SCOPE — exactly four items, nothing else read from the 2,034-line file

1. `modRMByte(Mod, RegOpcode, RM)` (~line 401) — `assert(...); return RM
   | (RegOpcode << 3) | (Mod << 6);`
2. `X86MCCodeEmitter::emitRegModRMByte` / `emitSIBByte` (~603-613) — both
   one-liners calling `modRMByte`.
3. The REX prefix machinery: `enum PrefixKind` (~line 41),
   `X86OpcodePrefixHelper::setR/setX/setB/setW` (one-line bodies, e.g.
   `void setR(unsigned Encoding) { R = Encoding >> 3 & 1; }`), and
   `emit(SmallVectorImpl<char> &CB)` — **only** the `case None:` /
   `case REX:` arms.
4. `emitByte(uint8_t C, SmallVectorImpl<char> &CB)`.

Everything else in the file — VEX/EVEX/XOP/REX2 prefix construction,
memory-operand ModRM/SIB (`emitMemModRMByte`), fixups/relocations, the
instruction dispatch table (`encodeInstruction`) — is **not visited** by
this transpiler at all. It is not "read and cut"; the extractors never
search for it.

## Cuts, with reachability invariants

- `X86OpcodePrefixHelper::emit`'s REX2/VEX2/VEX3/XOP/EVEX arms — CUT.
  **Invariant**: unreachable while only REX-form GPR instructions are
  exercised; no APX (REX2) or AVX/AVX-512/XOP instruction is ever driven
  through this transpile. Asserted at the cut site: any `Kind` other
  than `None`/`REX` raises `NotImplementedError` naming the violated
  invariant (checked directly in `test_agreement.py` part 4), never
  silently emits wrong or truncated bytes.
- Every field and method of `X86OpcodePrefixHelper` not listed in SCOPE
  item 3 (`M, R2, X2, B2, VEX_4V, VEX_L, VEX_PP, VEX_5M, EVEX_*`,
  `setR2/setX2/setB2/set4V/setL/setPP/set5M/setRR2/setM/setXX2/setBB2/
  setZ/setL2/setEVEX_b/setEVEX_U/setV2/set4VV2/setAAA/setNF/setSC/
  setLowerBound/determineOptimalKind/getRegEncoding`, and the real
  constructor's full field-initializer list) — CUT for the same
  invariant: they exist only to feed VEX/EVEX/XOP/REX2 construction.

## One documented judgment call: `getX86RegNum`

`emitRegModRMByte`'s literal one-liner body is:

```cpp
emitByte(modRMByte(3, RegOpcodeFld, getX86RegNum(ModRMReg)), CB);
```

`getX86RegNum(const MCOperand &MO)` is
`Ctx.getRegisterInfo()->getEncodingValue(MO.getReg()) & 0x7;` — it
depends on `MCContext`/`MCRegisterInfo`, an entire register-description
subsystem this slice does not model (transpiling it would mean pulling
in far more of LLVM's MC layer than the plan's four SCOPE items). The
transpiler elides that one call and takes the already-resolved 3-bit
register number as a parameter instead (`emit_reg_modrm_byte(
modrm_reg_num, reg_opcode_fld, cb)`), asserting the exact substring
`getX86RegNum(ModRMReg)` is present before substituting (so a source
change would fail loudly, not silently mis-transpile). This mirrors the
judgment call `vocab_support.py` already makes for `Gpr.enc()` — an
integer register encoding is accepted directly, without modelling
Cranelift's register-allocation machinery either. Not exercised by
`test_agreement.py`'s three ISA-fact checks (which only need
`mod_rm_byte`/the REX helper directly), so it's the one construct in
this file's SCOPE that is asserted-and-substituted rather than fully
tested.

## Outside the asserted domain (real, measured finding)

The plan asks: do `modRMByte` and `encode_modrm` also agree outside
their asserted domain? **They don't**, once you look past both
languages' guard mechanism:

- Rust's `debug_assert!` (what `encode_modrm` uses) is unconditionally
  compiled OUT of `--release` builds — Cranelift's normal shipping
  configuration. In release, `encode_modrm`'s masks (`& 3`, `& 7`) are
  what actually runs: out-of-range input is silently wrapped into range.
- C++'s `assert()` (what `modRMByte` uses) is compiled out only when
  `NDEBUG` is defined, which LLVM's `Release` configuration does define.
  In that build, `modRMByte`'s raw, **unmasked** arithmetic
  (`RM | (RegOpcode << 3) | (Mod << 6)`) is what runs: out-of-range
  input is not wrapped and can overflow a single byte's worth of bits
  entirely (e.g. `Mod=255, RegOpcode=255, RM=255` unmasked is `0x3fff`,
  not `0xff`).

Both `mod_rm_byte` (this file) and `encode_modrm` (`vocab_support.py`)
faithfully reproduce their source's guard as a plain Python `assert`, so
calling either guarded function out-of-domain just raises
`AssertionError` in both — which would look like agreement while hiding
the real difference. `test_agreement.py` part 1b bypasses both guards
explicitly and compares the two **core arithmetic formulas** directly,
which is the only way to see the divergence; see that test's inline
commentary for the five sampled cases and their results.

## `x++` / `->` policy checks (measured, not assumed)

- `x++` in argument position: the whole 2,034-line file was scanned for
  any `++`/`--` occurrence (111 found, all outside the four transpiled
  items — printed by every `transpile_cpp.py` run). None occur inside
  the transpiled slice, so the plan's split-on-increment rule never had
  to fire; the transpiler still asserts rather than assumes (see
  `transpile_cpp.py`'s module docstring) — it would raise `Unsupported`
  on an increment it can't safely split rather than silently mishandling
  one.
- `->` becomes `.`: the postfix parser (`ExprParser.parse_postfix`)
  treats `->` and `.` identically, but zero `->` occurrences exist in
  the transpiled slice — every object here is accessed by value or
  reference, never through a pointer.

## Uncertain / worth flagging

- The REX-byte check compares against `RexPrefix.mem_op`/`two_op` with
  `enc_reg`/`enc_rm` swept over the full 8-bit range (0–255), not just
  the 4-bit range (0–15) real x86-64 register encodings occupy. The
  formula (`Encoding >> 3 & 1`) is well-defined and agrees over the full
  swept range regardless, so this is a strictly stronger check than
  required, not a weaker one — but it means the "8-bit register
  encodings" phrasing in the acceptance gate is interpreted as "sweep
  the full byte", not "restrict to valid register numbers".
- `X86OpcodePrefixHelper.__init__`'s zero-initialization of
  `W`/`R`/`X`/`B` is not itself one of the four SCOPE items (the real
  constructor initializes 16 fields via an initializer list feeding
  VEX/EVEX state this transpile cuts) — it's the minimal bootstrapping
  needed for the four transpiled setters/`emit()` to be callable at all,
  documented in the class's `__init__` docstring rather than silently
  assumed.
