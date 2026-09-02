"""SLICE 2 — the encoder: CLIF instruction -> x86-64 bytes.

Transpiled from cranelift-assembler-x64 0.134.2:
    src/rex.rs          encode_modrm, RexPrefix (two_op/mem_op/
                        with_digit/encode)
    src/mem.rs          GprMem::as_rex_prefix, encode_rex_suffixes
    assembler.rs:38308  idivq_m::encode   (generated)
    assembler.rs:23577  cqto_zo::encode   (generated)

Cut from GENERATED Rust, never the DSL — same rule as ISLE.
No hand-written encoding: every byte below is produced by Rust's own
encode() logic re-expressed.
"""

# ---------------- gpr encodings (src/gpr.rs) ----------------
RAX, RCX, RDX, RBX, RSP, RBP, RSI, RDI = range(8)
R8, R9, R10, R11, R12, R13, R14, R15 = range(8, 16)


class CodeSink:
    """Stand-in for cranelift's CodeSink: collects bytes."""

    def __init__(self):
        self.buf = bytearray()

    def put1(self, b: int):
        self.buf.append(b & 0xFF)

    def add_trap(self, trap: str):
        pass          # traps are metadata, not bytes

    def bytes(self) -> bytes:
        return bytes(self.buf)


# ---------------- rex.rs ----------------

def encode_modrm(m0d: int, enc_reg_g: int, rm_e: int) -> int:
    assert m0d < 4 and enc_reg_g < 8 and rm_e < 8
    return ((m0d & 3) << 6) | ((enc_reg_g & 7) << 3) | (rm_e & 7)


def is_special_if_8bit(enc: int) -> bool:
    return 4 <= enc <= 7


class RexPrefix:
    def __init__(self, byte: int, must_emit: bool):
        self.byte = byte
        self.must_emit = must_emit

    @staticmethod
    def mem_op(enc_reg: int, enc_rm: int, w_bit: bool,
               uses_8bit: bool) -> "RexPrefix":
        must_emit = uses_8bit and is_special_if_8bit(enc_reg)
        w = 1 if w_bit else 0
        r = (enc_reg >> 3) & 1
        x = 0
        b = (enc_rm >> 3) & 1
        return RexPrefix(0x40 | (w << 3) | (r << 2) | (x << 1) | b,
                         must_emit)

    @staticmethod
    def two_op(enc_reg: int, enc_rm: int, w_bit: bool,
               uses_8bit: bool) -> "RexPrefix":
        ret = RexPrefix.mem_op(enc_reg, enc_rm, w_bit, uses_8bit)
        if uses_8bit and is_special_if_8bit(enc_rm):
            ret.must_emit = True
        return ret

    @staticmethod
    def with_digit(digit: int, enc_reg: int, w_bit: bool,
                   uses_8bit: bool) -> "RexPrefix":
        return RexPrefix.two_op(digit, enc_reg, w_bit, uses_8bit)

    def encode(self, sink: CodeSink):
        if self.byte != 0x40 or self.must_emit:
            sink.put1(self.byte)


# ---------------- mem.rs: GprMem (register form) ----------------

class GprMem:
    """GprMem::Gpr variant only — the memory (Amode) variants are cut;
    the i64 div path uses a register divisor."""

    def __init__(self, gpr: int):
        self.gpr = gpr

    def as_rex_prefix(self, enc_reg: int, has_w_bit: bool,
                      uses_8bit: bool) -> RexPrefix:
        return RexPrefix.two_op(enc_reg, self.gpr, has_w_bit, uses_8bit)

    def encode_rex_suffixes(self, sink: CodeSink, enc_reg: int,
                            bytes_at_end: int = 0, evex_scaling=None):
        sink.put1(encode_modrm(0b11, enc_reg & 0b111, self.gpr & 0b111))


# ---------------- generated instructions ----------------

class idivq_m:
    """assembler.rs:38285 — signed 64-bit divide, rm64 divisor."""

    def __init__(self, rax: int, rdx: int, rm64: GprMem,
                 trap: str = "INTEGER_DIVISION_BY_ZERO"):
        self.rax, self.rdx, self.rm64, self.trap = rax, rdx, rm64, trap

    def encode(self, buf: CodeSink):
        buf.add_trap(self.trap)
        uses_8bit = False
        w_bit = True
        digit = 0x7
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xF7)
        reg = 0x7
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)


class _RegRmOp:
    """Shared shape of addq_rm / subq_rm / imulq_rm (assembler.rs):
    REX(reg=r64, rm) + opcode(s) + ModRM. r64 is both source and
    destination."""

    OPCODE = ()          # subclasses set

    def __init__(self, r64: int, rm64: GprMem):
        self.r64, self.rm64 = r64, rm64

    def encode(self, buf: CodeSink):
        uses_8bit = False
        w_bit = True
        reg = self.r64
        rex = self.rm64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        for byte in self.OPCODE:
            buf.put1(byte)
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)


class addq_rm(_RegRmOp):
    """assembler.rs — add r64, rm64."""
    OPCODE = (0x03,)


class subq_rm(_RegRmOp):
    """assembler.rs — sub r64, rm64."""
    OPCODE = (0x2B,)


class imulq_rm(_RegRmOp):
    """assembler.rs — imul r64, rm64 (two-operand form)."""
    OPCODE = (0x0F, 0xAF)


class cqto_zo:
    """assembler.rs:23558 — sign-extend RAX into RDX:RAX (cqo)."""

    def __init__(self, rax: int = RAX, rdx: int = RDX):
        self.rax, self.rdx = rax, rdx

    def encode(self, buf: CodeSink):
        uses_8bit = False
        w_bit = True
        digit = 0
        dst = self.rdx
        rex = RexPrefix.with_digit(digit, dst, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x99)


# ---------------- convenience ----------------

def emit(*insts) -> bytes:
    sink = CodeSink()
    for inst in insts:
        inst.encode(sink)
    return sink.bytes()
