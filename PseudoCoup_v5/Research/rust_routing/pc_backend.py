"""The backend: assembles the transpiled slices into callable code.

    slice 1     routing    MIR binop + type  -> CLIF opcode
    slice 1.5   lowering   CLIF opcode       -> MInst sequence + result reg
    slice 2     encoding   MInst             -> x86-64 bytes
    output ring            bytes             -> mounted callable

Results are cached per (binop, type): routing runs once, the page is
mounted once, subsequent uses are a direct call.
"""

from slice_mir_routing import route
from slice_lowering import lower, QUOTIENT, REMAINDER
from slice_encoder import CodeSink, RSI
from output_ring import mount

# System V AMD64: arg0 -> RDI, arg1 -> RSI, return in RAX.
_PROLOGUE = bytes([0x48, 0x89, 0xF8])       # mov rax, rdi
_MOV_RAX_RDX = bytes([0x48, 0x89, 0xD0])    # mov rax, rdx
_RET = bytes([0xC3])

# Instruction sequences whose x86 trap conditions are guarded by
# Cranelift's CheckedDivOrRemSeq (emit.rs:215) — a slice we have NOT
# cut. Until it is cut, refuse the inputs it would have guarded
# rather than let the CPU fault. Trap canon (policy 8) either way.
_GUARDED = {"sdiv"}          # srem/urem now carry the emit.rs guard

_cache = {}


def _build_checked(clif_op, minsts, result_reg, divisor_reg):
    """Assemble the CheckedDivOrRemSeq guard (emit.rs:215).

    Two-pass label resolution: encode the parts, measure them, then
    emit with real displacements. No hand-written offset constants.
    """
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]
                          / "vocab_transpiler"))
    import pc_vocab
    from vocab_support import CodeSink as VSink, Gpr, GprMem, Imm, RDX

    def enc(inst):
        s = VSink(); inst.encode(s); return s.bytes()

    # --- the pieces, per emit.rs ---
    cmp_neg1 = enc(pc_vocab.cmpq_mi_sxb(GprMem(divisor_reg), Imm(0xFF, 1)))
    zero_dst = enc(pc_vocab.xorl_rm(Gpr(RDX), GprMem(RDX)))   # mov $0,%dst
    body = b"".join(enc(m) for m in minsts)

    # pass 1: measure. jne/jmp are 2 bytes each (rel8 forms).
    JCC_LEN = JMP_LEN = 2
    # jnz do_op : skip over [zero_dst + jmp]
    d_jnz = len(zero_dst) + JMP_LEN
    # jmp done : skip over [body]
    d_jmp = len(body)
    assert -128 <= d_jnz <= 127 and -128 <= d_jmp <= 127, \
        "rel8 displacement overflow — jne_d32/jmp_d32 not cut"

    # pass 2: emit with resolved displacements
    jnz = enc(pc_vocab.jne_d8(Imm(d_jnz, 1)))
    jmp = enc(pc_vocab.jmp_d8(Imm(d_jmp, 1)))
    assert len(jnz) == JCC_LEN and len(jmp) == JMP_LEN, \
        "rel8 length assumption violated"
    return cmp_neg1 + jnz + zero_dst + jmp + body


def compile_binop(bin_op: str, ty: str):
    key = (bin_op, ty)
    if key in _cache:
        return _cache[key]

    _, clif = route(bin_op, ty)                        # slice 1
    clif_op = clif[0][0]
    minsts, result_reg = lower(clif_op, ty, RSI)       # slice 1.5

    # ONLY srem carries the divisor==-1 guard (emit.rs
    # CheckedDivOrRemSeq). The guard exists because signed idiv
    # overflows on i64::MIN / -1. For UNSIGNED div, the bit pattern
    # 0xFFFF_FFFF_FFFF_FFFF is not -1 but u64::MAX, a perfectly
    # ordinary divisor — guarding it would wrongly return 0.
    # (Caught by the extended ground-truth grid: urem(a, u64::MAX)
    # returned 0 instead of a.)
    if clif_op == "srem":
        body = _build_checked(clif_op, minsts, result_reg, RSI)
    else:
        sink = CodeSink()                              # slice 2
        for inst in minsts:
            inst.encode(sink)
        body = sink.bytes()

    code = _PROLOGUE + body
    if result_reg == REMAINDER:
        code += _MOV_RAX_RDX
    code += _RET

    entry = {"clif": clif_op,
             "minsts": [type(m).__name__ for m in minsts],
             "result": "rdx" if result_reg == REMAINDER else "rax",
             "bytes": code,
             "mounted": mount(code)}
    _cache[key] = entry
    return entry


I64_MIN = -(1 << 63)


U64_MASK = (1 << 64) - 1


def call_binop(bin_op: str, ty: str, a: int, b: int) -> int:
    entry = compile_binop(bin_op, ty)
    if ty == "u64":
        if b == 0:
            raise ZeroDivisionError(f"{bin_op} by zero")
        # unsigned: operands cross as raw 64-bit patterns
        return entry["mounted"].call(
            (a & U64_MASK) - (1 << 64) if (a & U64_MASK) >= (1 << 63)
            else (a & U64_MASK),
            (b & U64_MASK) - (1 << 64) if (b & U64_MASK) >= (1 << 63)
            else (b & U64_MASK)) & U64_MASK
    if entry["clif"] in _GUARDED:
        if b == 0:
            raise ZeroDivisionError(
                f"{bin_op} by zero (Cranelift emits a trap here)")
        if b == -1 and a == I64_MIN:
            raise OverflowError(
                f"{bin_op}: i64::MIN / -1 overflows "
                f"(CheckedDivOrRemSeq guard not cut yet)")
    return entry["mounted"].call(a, b)


def cache_report():
    return {f"{op}/{ty}": {"clif": e["clif"],
                           "minsts": e["minsts"],
                           "result": e["result"],
                           "bytes": e["bytes"].hex(" ")}
            for (op, ty), e in _cache.items()}
