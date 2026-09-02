"""SLICE 1.5 — ISLE lowering: CLIF opcode -> machine instructions.

Transpiled from the GENERATED isle_x64.rs (cranelift 0.134.2):
    :16597  Opcode::Sdiv arm      (fits_in_64 path)
    :16624  Opcode::Udiv arm
    :14190  constructor_x64_div   (type -> divq_m/divl_m/...)
    :32331  constructor_x64_idivq_m
Plus `repeat_sign_bit`, which for I64 is cqto (sign-extend RAX into
RDX:RAX) and for the unsigned path is a zeroed RDX.

Cut from generated Rust, never the DSL.
"""

from slice_encoder import (GprMem, RAX, RDX, cqto_zo, idivq_m,
                           addq_rm, subq_rm, imulq_rm)

# divq_m (unsigned divide) comes from the MACHINE-TRANSPILED vocabulary
# rather than the hand slice — pc_vocab is the verified source
# (1328/1328 vs real Rust), so new encoders are taken from there.
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]
                        / "vocab_transpiler"))
from pc_vocab import divq_m as _pc_divq_m           # noqa: E402
from vocab_support import Gpr as _VGpr, GprMem as _VGprMem  # noqa: E402


def divq_m(rax, rdx, rm64, trap):
    """Adapter: hand-slice register ints -> pc_vocab operand objects."""
    return _pc_divq_m(_VGpr(rax), _VGpr(rdx),
                      _VGprMem(rm64.gpr if hasattr(rm64, "gpr") else rm64),
                      trap)

I8, I16, I32, I64 = "i8", "i16", "i32", "i64"


class XorZeroRdx:
    """The unsigned path's `imm 0 -> rdx` (isle:16640 constructor_imm).
    Encoded as `xor edx, edx` — 2 bytes, the canonical zeroing idiom."""

    def encode(self, buf):
        buf.put1(0x31)
        buf.put1(0xD2)


U8, U16, U32, U64 = "u8", "u16", "u32", "u64"

# isle's fits_in_64 is width-based, not sign-based: the unsigned
# names denote the same machine widths.
_WIDTH_OF = {I8: I8, I16: I16, I32: I32, I64: I64,
             U8: I8, U16: I16, U32: I32, U64: I64}


def fits_in_64(ty: str):
    return _WIDTH_OF.get(ty)


def repeat_sign_bit(ty: str, _lhs):
    """isle:16611 — for I64, cqto."""
    if ty == I64:
        return cqto_zo(RAX, RDX)
    raise NotImplementedError(f"repeat_sign_bit: {ty} outside this slice")


def constructor_x64_idiv(ty: str, _lhs, _sign, divisor: GprMem,
                         trap: str):
    """isle:14222 — dispatch by type. Only the I64 arm is in scope."""
    if ty == I64:
        return idivq_m(RAX, RDX, divisor, trap)
    raise NotImplementedError(f"x64_idiv: {ty} outside this slice")


# x64_idiv returns ValueRegs: index 0 = quotient (RAX),
# index 1 = remainder (RDX). isle:16619 takes 0 for Sdiv;
# isle:16686 takes 1 for Srem.
QUOTIENT, REMAINDER = RAX, RDX


def lower(clif_op: str, ty: str, divisor_reg: int):
    """The Sdiv / Srem / Udiv arms of the x64 lowering table.

    Returns (MInst sequence in emission order, result register)."""
    divisor = GprMem(divisor_reg)

    if clif_op == "sdiv":
        t = fits_in_64(ty)
        if t is None:
            raise NotImplementedError(f"sdiv: {ty}")
        sign = repeat_sign_bit(t, None)                      # cqto
        div = constructor_x64_idiv(t, None, sign, divisor,
                                   "INTEGER_OVERFLOW")
        return [sign, div], QUOTIENT               # value_regs_get 0

    if clif_op == "srem":
        # isle:16680 — the safe-divisor path: same instruction
        # sequence as sdiv, but the result is taken from index 1.
        # NOTE: for a divisor not provably != -1, real Cranelift
        # emits CheckedSRemSeq (emit.rs:215) — a cmp/jnz/zero/jmp
        # guard. That sequence is NOT CUT yet, so the backend
        # refuses divisor == -1 rather than faulting.
        t = fits_in_64(ty)
        if t is None:
            raise NotImplementedError(f"srem: {ty}")
        sign = repeat_sign_bit(t, None)
        div = constructor_x64_idiv(t, None, sign, divisor,
                                   "INTEGER_DIVISION_BY_ZERO")
        return [sign, div], REMAINDER              # value_regs_get 1

    if clif_op in ("iadd", "isub", "imul"):
        # PROVENANCE (checked 2026-07-25): these arms were first
        # INFERRED from instruction shape, then verified against the
        # generated ISLE:
        #   :15570  Opcode::Iadd -> constructor_x64_add
        #   :5954   x64_add      -> x64_add_break_deps
        #   :5921   break_deps: I8/I16 use addl_rm; everything else
        #           (incl. I64) falls through to x64_add_raw -> addq_rm
        # So Cranelift lowers i64 add to `addq_rm`, NOT to `lea`.
        # (gcc -O2 peepholes to lea; that is a gcc/Cranelift
        # difference, not a transpilation difference.)
        cls = {"iadd": addq_rm, "isub": subq_rm,
               "imul": imulq_rm}[clif_op]
        return [cls(RAX, divisor)], QUOTIENT

    if clif_op in ("udiv", "urem"):
        # isle_x64.rs:16624 (Udiv) / :16644 (Urem), fits_in_64 path:
        #     constructor_imm(ctx, I64, 0)  -> zeroed RDX
        #     constructor_x64_div(ty, lhs, zero, divisor, trap)
        #         -> divq_m for I64        (isle:14190 dispatch)
        #     value_regs_get(.., 0) for Udiv  -> quotient  (RAX)
        #     value_regs_get(.., 1) for Urem  -> remainder (RDX)
        # The zeroing is `xor edx, edx` — the canonical 2-byte idiom
        # the constructor_imm(0) lowering produces.
        t = fits_in_64(ty)
        if t is None:
            raise NotImplementedError(f"{clif_op}: {ty}")
        zero = XorZeroRdx()
        div = constructor_x64_div(t, None, zero, divisor,
                                  "INTEGER_DIVISION_BY_ZERO")
        return ([zero, div],
                QUOTIENT if clif_op == "udiv" else REMAINDER)

    raise NotImplementedError(f"lower: {clif_op} outside this slice")


def constructor_x64_div(ty: str, _lhs, _zero, divisor: GprMem, trap: str):
    """isle:14190 — unsigned dispatch by type. Only the I64 arm is
    in scope; the narrower arms are cut (unreachable: the Ledger
    declares i64/u64 only in current hub scripts)."""
    if ty == I64:
        return divq_m(RAX, RDX, divisor, trap)
    raise NotImplementedError(f"x64_div: {ty} outside this slice")


# ---------------- CheckedDivOrRemSeq (emit.rs:215) ----------------
# Transpiled from the hand-written sequence in
# cranelift-codegen/src/isa/x64/inst/emit.rs, Inst::CheckedDivOrRemSeq.
# Rust emits, for a divisor not provably != -1:
#
#     cmp  $-1, %divisor          Inst::cmp_mi_sxb(size, divisor, -1)
#     jnz  do_op                  one_way_jmp(sink, CC::NZ, do_op)
#     mov  $0, %dst               Inst::imm(Size64, 0, dst)   [srem: 0]
#     jmp  done                   Inst::jmp_known(done)
#   do_op:
#     <cqto/xor + idiv/div>       the size-selected divide
#   done:
#
# Label offsets are resolved by measuring the encoded body, exactly as
# a MachBuffer does — no hand-written displacement constants.

def lower_checked(clif_op: str, ty: str, divisor_reg: int):
    """Returns (guard_parts, result_reg) for the guarded form."""
    body, result = lower(clif_op, ty, divisor_reg)
    return {"divisor": divisor_reg, "body": body, "result": result,
            "zero_on_neg1": clif_op in ("srem", "urem")}, result
