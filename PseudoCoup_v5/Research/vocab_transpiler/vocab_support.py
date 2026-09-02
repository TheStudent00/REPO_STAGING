"""Support layer for the transpiled vocabulary — the SECOND grammar.

pc_vocab/*.py is mechanically transpiled from generated Rust (12 node
kinds, no arithmetic). This file is transpiled from the HAND-WRITTEN
Cranelift sources — rex.rs, mem.rs, gpr.rs — where the real arithmetic
lives, so this is where polyfills apply.

POLICY (the owner, 2026-07-25): UNIFORM wrapping. Every arithmetic node in a
u8-typed Rust expression is wrapped in u8(), with no exemptions — even
where overflow is provably impossible. Mixed depth would make an
unwrapped node ambiguous between "proven safe" and "tool missed it";
uniform depth makes an unwrapped node unambiguously a bug.
The exhaustive proofs become TESTS of these polyfills, not licence to
omit them.

Source: cranelift-assembler-x64 0.134.2
"""


# ---------------- polyfills (class-1, value-model) ----------------

def u8(x: int) -> int:
    return x & 0xFF


def u32(x: int) -> int:
    return x & 0xFFFFFFFF


# ---------------- CodeSink ----------------

class CodeSink:
    def __init__(self):
        self.buf = bytearray()
        self.traps = []

    def put1(self, b): self.buf.append(u8(b))

    def put2(self, v):
        v &= 0xFFFF
        self.buf += bytes((v & 0xFF, (v >> 8) & 0xFF))

    def put4(self, v):
        v = u32(v)
        self.buf += v.to_bytes(4, "little")

    def put8(self, v):
        self.buf += (v & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little")

    def add_trap(self, code): self.traps.append(code)

    def bytes(self): return bytes(self.buf)


# ---------------- rex.rs ----------------

def encode_modrm(m0d, enc_reg_g, rm_e):
    assert m0d < 4 and enc_reg_g < 8 and rm_e < 8      # debug_assert!
    return u8(u8(u8(m0d & 3) << 6) | u8(u8(enc_reg_g & 7) << 3)
              | u8(rm_e & 7))


def encode_sib(scale, enc_index, enc_base):
    assert scale < 4 and enc_index < 8 and enc_base < 8
    return u8(u8(u8(scale & 3) << 6) | u8(u8(enc_index & 7) << 3)
              | u8(enc_base & 7))


def is_special_if_8bit(enc):
    return 4 <= enc <= 7


class RexPrefix:
    __slots__ = ("byte", "must_emit")

    def __init__(self, byte, must_emit):
        self.byte, self.must_emit = byte, must_emit

    @staticmethod
    def one_op(enc, w_bit, uses_8bit):
        must_emit = uses_8bit and is_special_if_8bit(enc)
        w = 1 if w_bit else 0
        r = 0
        x = 0
        b = u8(u8(enc >> 3) & 1)
        return RexPrefix(u8(0x40 | u8(w << 3) | u8(r << 2) | u8(x << 1) | b),
                         must_emit)

    @staticmethod
    def mem_op(enc_reg, enc_rm, w_bit, uses_8bit):
        must_emit = uses_8bit and is_special_if_8bit(enc_reg)
        w = 1 if w_bit else 0
        r = u8(u8(enc_reg >> 3) & 1)
        x = 0
        b = u8(u8(enc_rm >> 3) & 1)
        return RexPrefix(u8(0x40 | u8(w << 3) | u8(r << 2) | u8(x << 1) | b),
                         must_emit)

    @staticmethod
    def two_op(enc_reg, enc_rm, w_bit, uses_8bit):
        ret = RexPrefix.mem_op(enc_reg, enc_rm, w_bit, uses_8bit)
        if uses_8bit and is_special_if_8bit(enc_rm):
            ret.must_emit = True
        return ret

    @staticmethod
    def with_digit(digit, enc_reg, w_bit, uses_8bit):
        return RexPrefix.two_op(digit, enc_reg, w_bit, uses_8bit)

    @staticmethod
    def three_op(enc_reg, enc_index, enc_base, w_bit, uses_8bit):
        must_emit = uses_8bit and is_special_if_8bit(enc_reg)
        w = 1 if w_bit else 0
        r = u8(u8(enc_reg >> 3) & 1)
        x = u8(u8(enc_index >> 3) & 1)
        b = u8(u8(enc_base >> 3) & 1)
        return RexPrefix(u8(0x40 | u8(w << 3) | u8(r << 2) | u8(x << 1) | b),
                         must_emit)

    def encode(self, sink):
        if self.byte != 0x40 or self.must_emit:
            sink.put1(self.byte)


# ---------------- gpr.rs / operands ----------------

RAX, RCX, RDX, RBX, RSP, RBP, RSI, RDI = range(8)
R8, R9, R10, R11, R12, R13, R14, R15 = range(8, 16)


class Gpr:
    """A general-purpose register operand. Also serves as the Fixed<>
    wrapper the generated code sees for rax/rdx-pinned operands."""
    __slots__ = ("_enc",)

    def __init__(self, enc):
        self._enc = int(enc)

    def enc(self):
        enc = self._enc
        assert enc < 16, f"invalid register: {enc}"      # gpr.rs:26
        return enc

    def trap_code(self):
        return None

    def encode_modrm(self, sink, enc_reg):
        """xmm.rs:35 — emit this register as the r/m field."""
        sink.put1(encode_modrm(0b11, u8(enc_reg & 0b111),
                               u8(self.enc() & 0b111)))

    def encode_bx_regs(self):
        """xmm.rs — single register: only the b bit is set."""
        return (self.enc(), None)

    def as_rex_prefix(self, enc_reg, has_w_bit, uses_8bit):
        return RexPrefix.two_op(enc_reg, self.enc(), has_w_bit, uses_8bit)

    def encode_rex_suffixes(self, sink, enc_reg, bytes_at_end=0,
                            evex_scaling=None):
        self.encode_modrm(sink, enc_reg)

    def __repr__(self):
        return f"Gpr({self._enc})"


class Mem:
    """Memory operand (Amode). CUT — see reachability note below."""
    __slots__ = ("_trap",)

    def __init__(self, trap=None):
        self._trap = trap

    def trap_code(self):
        return self._trap


class GprMem:
    """GprMem::Gpr | GprMem::Mem.

    CUT + REACHABILITY INVARIANT: the Mem arm is not transpiled.
    It is unreachable while every caller constructs register operands
    (true for all current slices: register allocation with spills is
    not cut). The invariant is asserted, not assumed — if a Mem
    operand ever arrives, this fails loudly at the cut site rather
    than emitting wrong bytes.
    """
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value if isinstance(value, (Gpr, Mem)) else Gpr(value)

    def _require_gpr(self):
        if isinstance(self.value, Mem):
            raise NotImplementedError(
                "GprMem::Mem arm not cut (Amode encoding). Invariant "
                "'all callers use register operands' has been violated.")
        return self.value

    def trap_code(self):
        return self.value.trap_code()

    def as_rex_prefix(self, enc_reg, has_w_bit, uses_8bit):
        rm = self._require_gpr()
        return RexPrefix.two_op(enc_reg, rm.enc(), has_w_bit, uses_8bit)

    def encode_rex_suffixes(self, sink, enc_reg, bytes_at_end=0,
                            evex_scaling=None):
        gpr = self._require_gpr()
        sink.put1(encode_modrm(0b11, u8(enc_reg & 0b111),
                               u8(gpr.enc() & 0b111)))

    def encode_bx_regs(self):
        return (self._require_gpr().enc(), None)


# XmmMem shares GprMem's shape for the paths we reach.
XmmMem = GprMem
Xmm = Gpr


# ---------------- cuts: SIMD prefixes ----------------

class _CutPrefix:
    """VEX/EVEX prefixes — NOT CUT.

    REACHABILITY INVARIANT: reachable only from AVX/AVX-512
    instructions. No current slice emits those; the GPR integer
    vocabulary never constructs one.
    """
    @staticmethod
    def _cut(*_a, **_k):
        raise NotImplementedError(
            "VEX/EVEX prefix encoding not cut (SIMD path). Invariant "
            "'no AVX instruction is reached' has been violated.")

    two_op = three_op = _cut


VexPrefix = _CutPrefix
EvexPrefix = _CutPrefix


class Imm:
    """Immediate operand; width from the constructor."""
    __slots__ = ("value", "width")

    def __init__(self, value, width=4):
        self.value, self.width = int(value), width

    def encode(self, sink):
        {1: sink.put1, 2: sink.put2, 4: sink.put4,
         8: sink.put8}[self.width](self.value)

    def trap_code(self):
        return None

class _CustomEncode:
    """Transpiled from custom.rs — the generated file's escape hatch.

    Handles put1/put2/put4/put8 uniformly. The first version of this
    block matched only put1 and silently dropped put2/put4, which the
    full differential test caught as 10 byte mismatches (nop_5b..9b).
    """
    @staticmethod
    def nop_1b(_inst, buf):
        buf.put1(0x90)
    @staticmethod
    def nop_2b(_inst, buf):
        buf.put1(0x66)
        buf.put1(0x90)
    @staticmethod
    def nop_3b(_inst, buf):
        buf.put1(0x0f)
        buf.put1(0x1f)
        buf.put1(0x00)
    @staticmethod
    def nop_4b(_inst, buf):
        buf.put1(0x0f)
        buf.put1(0x1f)
        buf.put1(0x40)
        buf.put1(0x00)
    @staticmethod
    def nop_5b(_inst, buf):
        buf.put1(0x0f)
        buf.put1(0x1f)
        buf.put1(0x44)
        buf.put2(0x0000)
    @staticmethod
    def nop_6b(_inst, buf):
        buf.put1(0x66)
        buf.put1(0x0f)
        buf.put1(0x1f)
        buf.put1(0x44)
        buf.put2(0x0000)
    @staticmethod
    def nop_7b(_inst, buf):
        buf.put1(0x0f)
        buf.put1(0x1f)
        buf.put1(0x80)
        buf.put4(0x00000000)
    @staticmethod
    def nop_8b(_inst, buf):
        buf.put1(0x0f)
        buf.put1(0x1f)
        buf.put1(0x84)
        buf.put1(0x00)
        buf.put4(0x00000000)
    @staticmethod
    def nop_9b(_inst, buf):
        buf.put1(0x66)
        buf.put1(0x0f)
        buf.put1(0x1f)
        buf.put1(0x84)
        buf.put1(0x00)
        buf.put4(0x00000000)

custom_encode = _CustomEncode()
