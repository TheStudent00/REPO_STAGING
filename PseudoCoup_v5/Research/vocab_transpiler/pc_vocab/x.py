"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class xchgb_rm:
    """xchgb"""
    MNEMONIC = 'xchgb'
    FIELDS = ('r8', 'm8')

    def __init__(self, r8, m8):
        self.r8 = r8
        self.m8 = m8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        uses_8bit = True
        w_bit = False
        reg = self.r8.enc()
        rex = self.m8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x86)
        reg = self.r8.enc()
        self.m8.encode_rex_suffixes(buf, reg, 0, None)

class xchgw_rm:
    """xchgw"""
    MNEMONIC = 'xchgw'
    FIELDS = ('r16', 'm16')

    def __init__(self, r16, m16):
        self.r16 = r16
        self.m16 = m16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.r16.enc()
        rex = self.m16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x87)
        reg = self.r16.enc()
        self.m16.encode_rex_suffixes(buf, reg, 0, None)

class xchgl_rm:
    """xchgl"""
    MNEMONIC = 'xchgl'
    FIELDS = ('r32', 'm32')

    def __init__(self, r32, m32):
        self.r32 = r32
        self.m32 = m32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x87)
        reg = self.r32.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class xchgq_rm:
    """xchgq"""
    MNEMONIC = 'xchgq'
    FIELDS = ('r64', 'm64')

    def __init__(self, r64, m64):
        self.r64 = r64
        self.m64 = m64

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x87)
        reg = self.r64.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class xorb_i:
    """xorb"""
    MNEMONIC = 'xorb'
    FIELDS = ('al', 'imm8')

    def __init__(self, al, imm8):
        self.al = al
        self.imm8 = imm8

    def encode(self, buf):
        uses_8bit = False
        w_bit = False
        digit = 0
        dst = self.al.enc()
        rex = RexPrefix.with_digit(digit, dst, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x34)
        self.imm8.encode(buf)

class xorw_i:
    """xorw"""
    MNEMONIC = 'xorw'
    FIELDS = ('ax', 'imm16')

    def __init__(self, ax, imm16):
        self.ax = ax
        self.imm16 = imm16

    def encode(self, buf):
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        digit = 0
        dst = self.ax.enc()
        rex = RexPrefix.with_digit(digit, dst, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x35)
        self.imm16.encode(buf)

class xorl_i:
    """xorl"""
    MNEMONIC = 'xorl'
    FIELDS = ('eax', 'imm32')

    def __init__(self, eax, imm32):
        self.eax = eax
        self.imm32 = imm32

    def encode(self, buf):
        uses_8bit = False
        w_bit = False
        digit = 0
        dst = self.eax.enc()
        rex = RexPrefix.with_digit(digit, dst, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x35)
        self.imm32.encode(buf)

class xorq_i_sxl:
    """xorq"""
    MNEMONIC = 'xorq'
    FIELDS = ('rax', 'imm32')

    def __init__(self, rax, imm32):
        self.rax = rax
        self.imm32 = imm32

    def encode(self, buf):
        uses_8bit = False
        w_bit = True
        digit = 0
        dst = self.rax.enc()
        rex = RexPrefix.with_digit(digit, dst, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x35)
        self.imm32.encode(buf)

class xorb_mi:
    """xorb"""
    MNEMONIC = 'xorb'
    FIELDS = ('rm8', 'imm8')

    def __init__(self, rm8, imm8):
        self.rm8 = rm8
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.rm8, Mem):
            rm8 = self.rm8
            trap_code = rm8.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = True
        w_bit = False
        digit = 0x6
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x80)
        reg = 0x6
        self.rm8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class xorw_mi:
    """xorw"""
    MNEMONIC = 'xorw'
    FIELDS = ('rm16', 'imm16')

    def __init__(self, rm16, imm16):
        self.rm16 = rm16
        self.imm16 = imm16

    def encode(self, buf):
        if isinstance(self.rm16, Mem):
            rm16 = self.rm16
            trap_code = rm16.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        digit = 0x6
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x6
        self.rm16.encode_rex_suffixes(buf, reg, 2, None)
        self.imm16.encode(buf)

class xorl_mi:
    """xorl"""
    MNEMONIC = 'xorl'
    FIELDS = ('rm32', 'imm32')

    def __init__(self, rm32, imm32):
        self.rm32 = rm32
        self.imm32 = imm32

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = False
        digit = 0x6
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x6
        self.rm32.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class xorq_mi_sxl:
    """xorq"""
    MNEMONIC = 'xorq'
    FIELDS = ('rm64', 'imm32')

    def __init__(self, rm64, imm32):
        self.rm64 = rm64
        self.imm32 = imm32

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = True
        digit = 0x6
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x6
        self.rm64.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class xorl_mi_sxb:
    """xorl"""
    MNEMONIC = 'xorl'
    FIELDS = ('rm32', 'imm8')

    def __init__(self, rm32, imm8):
        self.rm32 = rm32
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = False
        digit = 0x6
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x6
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class xorq_mi_sxb:
    """xorq"""
    MNEMONIC = 'xorq'
    FIELDS = ('rm64', 'imm8')

    def __init__(self, rm64, imm8):
        self.rm64 = rm64
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = True
        digit = 0x6
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x6
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class xorb_mr:
    """xorb"""
    MNEMONIC = 'xorb'
    FIELDS = ('rm8', 'r8')

    def __init__(self, rm8, r8):
        self.rm8 = rm8
        self.r8 = r8

    def encode(self, buf):
        if isinstance(self.rm8, Mem):
            rm8 = self.rm8
            trap_code = rm8.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = True
        w_bit = False
        reg = self.r8.enc()
        rex = self.rm8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x30)
        reg = self.r8.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class xorw_mr:
    """xorw"""
    MNEMONIC = 'xorw'
    FIELDS = ('rm16', 'r16')

    def __init__(self, rm16, r16):
        self.rm16 = rm16
        self.r16 = r16

    def encode(self, buf):
        if isinstance(self.rm16, Mem):
            rm16 = self.rm16
            trap_code = rm16.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.r16.enc()
        rex = self.rm16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x31)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class xorl_mr:
    """xorl"""
    MNEMONIC = 'xorl'
    FIELDS = ('rm32', 'r32')

    def __init__(self, rm32, r32):
        self.rm32 = rm32
        self.r32 = r32

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.rm32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x31)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class xorq_mr:
    """xorq"""
    MNEMONIC = 'xorq'
    FIELDS = ('rm64', 'r64')

    def __init__(self, rm64, r64):
        self.rm64 = rm64
        self.r64 = r64

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.rm64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x31)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class xorb_rm:
    """xorb"""
    MNEMONIC = 'xorb'
    FIELDS = ('r8', 'rm8')

    def __init__(self, r8, rm8):
        self.r8 = r8
        self.rm8 = rm8

    def encode(self, buf):
        if isinstance(self.rm8, Mem):
            rm8 = self.rm8
            trap_code = rm8.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = True
        w_bit = False
        reg = self.r8.enc()
        rex = self.rm8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x32)
        reg = self.r8.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class xorw_rm:
    """xorw"""
    MNEMONIC = 'xorw'
    FIELDS = ('r16', 'rm16')

    def __init__(self, r16, rm16):
        self.r16 = r16
        self.rm16 = rm16

    def encode(self, buf):
        if isinstance(self.rm16, Mem):
            rm16 = self.rm16
            trap_code = rm16.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.r16.enc()
        rex = self.rm16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x33)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class xorl_rm:
    """xorl"""
    MNEMONIC = 'xorl'
    FIELDS = ('r32', 'rm32')

    def __init__(self, r32, rm32):
        self.r32 = r32
        self.rm32 = rm32

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.rm32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x33)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class xorq_rm:
    """xorq"""
    MNEMONIC = 'xorq'
    FIELDS = ('r64', 'rm64')

    def __init__(self, r64, rm64):
        self.r64 = r64
        self.rm64 = rm64

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.rm64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x33)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class xorps_a:
    """xorps"""
    MNEMONIC = 'xorps'
    FIELDS = ('xmm1', 'xmm_m128')

    def __init__(self, xmm1, xmm_m128):
        self.xmm1 = xmm1
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m128.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x57)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class xorpd_a:
    """xorpd"""
    MNEMONIC = 'xorpd'
    FIELDS = ('xmm1', 'xmm_m128')

    def __init__(self, xmm1, xmm_m128):
        self.xmm1 = xmm1
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m128.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x57)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)
