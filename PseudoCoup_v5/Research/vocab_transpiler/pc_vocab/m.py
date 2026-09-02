"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class movmskps_rm:
    """movmskps"""
    MNEMONIC = 'movmskps'
    FIELDS = ('r32', 'xmm2')

    def __init__(self, r32, xmm2):
        self.r32 = r32
        self.xmm2 = xmm2

    def encode(self, buf):
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rm = self.xmm2.enc()
        rex = RexPrefix.two_op(reg, rm, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x50)
        reg = self.r32.enc()
        self.xmm2.encode_modrm(buf, reg)

class movmskpd_rm:
    """movmskpd"""
    MNEMONIC = 'movmskpd'
    FIELDS = ('r32', 'xmm2')

    def __init__(self, r32, xmm2):
        self.r32 = r32
        self.xmm2 = xmm2

    def encode(self, buf):
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rm = self.xmm2.enc()
        rex = RexPrefix.two_op(reg, rm, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x50)
        reg = self.r32.enc()
        self.xmm2.encode_modrm(buf, reg)

class movhps_a:
    """movhps"""
    MNEMONIC = 'movhps'
    FIELDS = ('xmm1', 'm64')

    def __init__(self, xmm1, m64):
        self.xmm1 = xmm1
        self.m64 = m64

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x16)
        reg = self.xmm1.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class movlhps_rm:
    """movlhps"""
    MNEMONIC = 'movlhps'
    FIELDS = ('xmm1', 'xmm2')

    def __init__(self, xmm1, xmm2):
        self.xmm1 = xmm1
        self.xmm2 = xmm2

    def encode(self, buf):
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rm = self.xmm2.enc()
        rex = RexPrefix.two_op(reg, rm, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x16)
        reg = self.xmm1.enc()
        self.xmm2.encode_modrm(buf, reg)

class movddup_a:
    """movddup"""
    MNEMONIC = 'movddup'
    FIELDS = ('xmm1', 'xmm_m64')

    def __init__(self, xmm1, xmm_m64):
        self.xmm1 = xmm1
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0xF2)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x12)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class maxss_a:
    """maxss"""
    MNEMONIC = 'maxss'
    FIELDS = ('xmm1', 'xmm_m32')

    def __init__(self, xmm1, xmm_m32):
        self.xmm1 = xmm1
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x5f)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class maxsd_a:
    """maxsd"""
    MNEMONIC = 'maxsd'
    FIELDS = ('xmm1', 'xmm_m64')

    def __init__(self, xmm1, xmm_m64):
        self.xmm1 = xmm1
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0xF2)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x5f)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class maxps_a:
    """maxps"""
    MNEMONIC = 'maxps'
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
        buf.put1(0x5f)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class maxpd_a:
    """maxpd"""
    MNEMONIC = 'maxpd'
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
        buf.put1(0x5f)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class minss_a:
    """minss"""
    MNEMONIC = 'minss'
    FIELDS = ('xmm1', 'xmm_m32')

    def __init__(self, xmm1, xmm_m32):
        self.xmm1 = xmm1
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x5d)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class minsd_a:
    """minsd"""
    MNEMONIC = 'minsd'
    FIELDS = ('xmm1', 'xmm_m64')

    def __init__(self, xmm1, xmm_m64):
        self.xmm1 = xmm1
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0xF2)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x5d)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class minps_a:
    """minps"""
    MNEMONIC = 'minps'
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
        buf.put1(0x5d)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class minpd_a:
    """minpd"""
    MNEMONIC = 'minpd'
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
        buf.put1(0x5d)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class mfence_zo:
    """mfence"""
    MNEMONIC = 'mfence'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0xae)
        buf.put1(0xf0)

class movb_mr:
    """movb"""
    MNEMONIC = 'movb'
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
        buf.put1(0x88)
        reg = self.r8.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class movw_mr:
    """movw"""
    MNEMONIC = 'movw'
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
        buf.put1(0x89)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class movl_mr:
    """movl"""
    MNEMONIC = 'movl'
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
        buf.put1(0x89)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class movq_mr:
    """movq"""
    MNEMONIC = 'movq'
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
        buf.put1(0x89)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class movb_rm:
    """movb"""
    MNEMONIC = 'movb'
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
        buf.put1(0x8a)
        reg = self.r8.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class movw_rm:
    """movw"""
    MNEMONIC = 'movw'
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
        buf.put1(0x8b)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class movl_rm:
    """movl"""
    MNEMONIC = 'movl'
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
        buf.put1(0x8b)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class movq_rm:
    """movq"""
    MNEMONIC = 'movq'
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
        buf.put1(0x8b)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class movb_oi:
    """movb"""
    MNEMONIC = 'movb'
    FIELDS = ('r8', 'imm8')

    def __init__(self, r8, imm8):
        self.r8 = r8
        self.imm8 = imm8

    def encode(self, buf):
        uses_8bit = True
        w_bit = False
        dst = self.r8.enc()
        rex = RexPrefix.one_op(dst, w_bit, uses_8bit)
        rex.encode(buf)
        low_bits = self.r8.enc() & 0b111
        buf.put1(0xb0 | low_bits)
        self.imm8.encode(buf)

class movw_oi:
    """movw"""
    MNEMONIC = 'movw'
    FIELDS = ('r16', 'imm16')

    def __init__(self, r16, imm16):
        self.r16 = r16
        self.imm16 = imm16

    def encode(self, buf):
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        dst = self.r16.enc()
        rex = RexPrefix.one_op(dst, w_bit, uses_8bit)
        rex.encode(buf)
        low_bits = self.r16.enc() & 0b111
        buf.put1(0xb8 | low_bits)
        self.imm16.encode(buf)

class movl_oi:
    """movl"""
    MNEMONIC = 'movl'
    FIELDS = ('r32', 'imm32')

    def __init__(self, r32, imm32):
        self.r32 = r32
        self.imm32 = imm32

    def encode(self, buf):
        uses_8bit = False
        w_bit = False
        dst = self.r32.enc()
        rex = RexPrefix.one_op(dst, w_bit, uses_8bit)
        rex.encode(buf)
        low_bits = self.r32.enc() & 0b111
        buf.put1(0xb8 | low_bits)
        self.imm32.encode(buf)

class movabsq_oi:
    """movabsq"""
    MNEMONIC = 'movabsq'
    FIELDS = ('r64', 'imm64')

    def __init__(self, r64, imm64):
        self.r64 = r64
        self.imm64 = imm64

    def encode(self, buf):
        uses_8bit = False
        w_bit = True
        dst = self.r64.enc()
        rex = RexPrefix.one_op(dst, w_bit, uses_8bit)
        rex.encode(buf)
        low_bits = self.r64.enc() & 0b111
        buf.put1(0xb8 | low_bits)
        self.imm64.encode(buf)

class movb_mi:
    """movb"""
    MNEMONIC = 'movb'
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
        digit = 0x0
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc6)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class movw_mi:
    """movw"""
    MNEMONIC = 'movw'
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
        digit = 0x0
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc7)
        reg = 0x0
        self.rm16.encode_rex_suffixes(buf, reg, 2, None)
        self.imm16.encode(buf)

class movl_mi:
    """movl"""
    MNEMONIC = 'movl'
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
        digit = 0x0
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc7)
        reg = 0x0
        self.rm32.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class movq_mi_sxl:
    """movq"""
    MNEMONIC = 'movq'
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
        digit = 0x0
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc7)
        reg = 0x0
        self.rm64.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class movsbw_rm:
    """movsbw"""
    MNEMONIC = 'movsbw'
    FIELDS = ('r16', 'rm8')

    def __init__(self, r16, rm8):
        self.r16 = r16
        self.rm8 = rm8

    def encode(self, buf):
        if isinstance(self.rm8, Mem):
            rm8 = self.rm8
            trap_code = rm8.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0x66)
        uses_8bit = True
        w_bit = False
        reg = self.r16.enc()
        rex = self.rm8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xbe)
        reg = self.r16.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class movsbl_rm:
    """movsbl"""
    MNEMONIC = 'movsbl'
    FIELDS = ('r32', 'rm8')

    def __init__(self, r32, rm8):
        self.r32 = r32
        self.rm8 = rm8

    def encode(self, buf):
        if isinstance(self.rm8, Mem):
            rm8 = self.rm8
            trap_code = rm8.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = True
        w_bit = False
        reg = self.r32.enc()
        rex = self.rm8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xbe)
        reg = self.r32.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class movsbq_rm:
    """movsbq"""
    MNEMONIC = 'movsbq'
    FIELDS = ('r64', 'rm8')

    def __init__(self, r64, rm8):
        self.r64 = r64
        self.rm8 = rm8

    def encode(self, buf):
        if isinstance(self.rm8, Mem):
            rm8 = self.rm8
            trap_code = rm8.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = True
        w_bit = True
        reg = self.r64.enc()
        rex = self.rm8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xbe)
        reg = self.r64.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class movsww_rm:
    """movsww"""
    MNEMONIC = 'movsww'
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
        buf.put1(0x0f)
        buf.put1(0xbf)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class movswl_rm:
    """movswl"""
    MNEMONIC = 'movswl'
    FIELDS = ('r32', 'rm16')

    def __init__(self, r32, rm16):
        self.r32 = r32
        self.rm16 = rm16

    def encode(self, buf):
        if isinstance(self.rm16, Mem):
            rm16 = self.rm16
            trap_code = rm16.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.rm16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xbf)
        reg = self.r32.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class movswq_rm:
    """movswq"""
    MNEMONIC = 'movswq'
    FIELDS = ('r64', 'rm16')

    def __init__(self, r64, rm16):
        self.r64 = r64
        self.rm16 = rm16

    def encode(self, buf):
        if isinstance(self.rm16, Mem):
            rm16 = self.rm16
            trap_code = rm16.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.rm16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xbf)
        reg = self.r64.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class movslq_rm:
    """movslq"""
    MNEMONIC = 'movslq'
    FIELDS = ('r64', 'rm32')

    def __init__(self, r64, rm32):
        self.r64 = r64
        self.rm32 = rm32

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.rm32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x63)
        reg = self.r64.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class movzbw_rm:
    """movzbw"""
    MNEMONIC = 'movzbw'
    FIELDS = ('r16', 'rm8')

    def __init__(self, r16, rm8):
        self.r16 = r16
        self.rm8 = rm8

    def encode(self, buf):
        if isinstance(self.rm8, Mem):
            rm8 = self.rm8
            trap_code = rm8.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0x66)
        uses_8bit = True
        w_bit = False
        reg = self.r16.enc()
        rex = self.rm8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xb6)
        reg = self.r16.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class movzbl_rm:
    """movzbl"""
    MNEMONIC = 'movzbl'
    FIELDS = ('r32', 'rm8')

    def __init__(self, r32, rm8):
        self.r32 = r32
        self.rm8 = rm8

    def encode(self, buf):
        if isinstance(self.rm8, Mem):
            rm8 = self.rm8
            trap_code = rm8.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = True
        w_bit = False
        reg = self.r32.enc()
        rex = self.rm8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xb6)
        reg = self.r32.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class movzbq_rm:
    """movzbq"""
    MNEMONIC = 'movzbq'
    FIELDS = ('r64', 'rm8')

    def __init__(self, r64, rm8):
        self.r64 = r64
        self.rm8 = rm8

    def encode(self, buf):
        if isinstance(self.rm8, Mem):
            rm8 = self.rm8
            trap_code = rm8.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = True
        w_bit = True
        reg = self.r64.enc()
        rex = self.rm8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xb6)
        reg = self.r64.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class movzww_rm:
    """movzww"""
    MNEMONIC = 'movzww'
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
        buf.put1(0x0f)
        buf.put1(0xb7)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class movzwl_rm:
    """movzwl"""
    MNEMONIC = 'movzwl'
    FIELDS = ('r32', 'rm16')

    def __init__(self, r32, rm16):
        self.r32 = r32
        self.rm16 = rm16

    def encode(self, buf):
        if isinstance(self.rm16, Mem):
            rm16 = self.rm16
            trap_code = rm16.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.rm16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xb7)
        reg = self.r32.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class movzwq_rm:
    """movzwq"""
    MNEMONIC = 'movzwq'
    FIELDS = ('r64', 'rm16')

    def __init__(self, r64, rm16):
        self.r64 = r64
        self.rm16 = rm16

    def encode(self, buf):
        if isinstance(self.rm16, Mem):
            rm16 = self.rm16
            trap_code = rm16.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.rm16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xb7)
        reg = self.r64.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class movd_a:
    """movd"""
    MNEMONIC = 'movd'
    FIELDS = ('xmm1', 'rm32')

    def __init__(self, xmm1, rm32):
        self.xmm1 = xmm1
        self.rm32 = rm32

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.rm32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x6e)
        reg = self.xmm1.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class movq_a:
    """movq"""
    MNEMONIC = 'movq'
    FIELDS = ('xmm1', 'rm64')

    def __init__(self, xmm1, rm64):
        self.xmm1 = xmm1
        self.rm64 = rm64

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = True
        reg = self.xmm1.enc()
        rex = self.rm64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x6e)
        reg = self.xmm1.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class movd_b:
    """movd"""
    MNEMONIC = 'movd'
    FIELDS = ('rm32', 'xmm2')

    def __init__(self, rm32, xmm2):
        self.rm32 = rm32
        self.xmm2 = xmm2

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.xmm2.enc()
        rex = self.rm32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x7e)
        reg = self.xmm2.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class movq_b:
    """movq"""
    MNEMONIC = 'movq'
    FIELDS = ('rm64', 'xmm2')

    def __init__(self, rm64, xmm2):
        self.rm64 = rm64
        self.xmm2 = xmm2

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = True
        reg = self.xmm2.enc()
        rex = self.rm64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x7e)
        reg = self.xmm2.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class movss_a_m:
    """movss"""
    MNEMONIC = 'movss'
    FIELDS = ('xmm1', 'm32')

    def __init__(self, xmm1, m32):
        self.xmm1 = xmm1
        self.m32 = m32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x10)
        reg = self.xmm1.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class movss_a_r:
    """movss"""
    MNEMONIC = 'movss'
    FIELDS = ('xmm1', 'xmm2')

    def __init__(self, xmm1, xmm2):
        self.xmm1 = xmm1
        self.xmm2 = xmm2

    def encode(self, buf):
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rm = self.xmm2.enc()
        rex = RexPrefix.two_op(reg, rm, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x10)
        reg = self.xmm1.enc()
        self.xmm2.encode_modrm(buf, reg)

class movss_c_m:
    """movss"""
    MNEMONIC = 'movss'
    FIELDS = ('m32', 'xmm1')

    def __init__(self, m32, xmm1):
        self.m32 = m32
        self.xmm1 = xmm1

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x11)
        reg = self.xmm1.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class movsd_a_m:
    """movsd"""
    MNEMONIC = 'movsd'
    FIELDS = ('xmm1', 'm64')

    def __init__(self, xmm1, m64):
        self.xmm1 = xmm1
        self.m64 = m64

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF2)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x10)
        reg = self.xmm1.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class movsd_a_r:
    """movsd"""
    MNEMONIC = 'movsd'
    FIELDS = ('xmm1', 'xmm2')

    def __init__(self, xmm1, xmm2):
        self.xmm1 = xmm1
        self.xmm2 = xmm2

    def encode(self, buf):
        buf.put1(0xF2)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rm = self.xmm2.enc()
        rex = RexPrefix.two_op(reg, rm, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x10)
        reg = self.xmm1.enc()
        self.xmm2.encode_modrm(buf, reg)

class movsd_c_m:
    """movsd"""
    MNEMONIC = 'movsd'
    FIELDS = ('m64', 'xmm1')

    def __init__(self, m64, xmm1):
        self.m64 = m64
        self.xmm1 = xmm1

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF2)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x11)
        reg = self.xmm1.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class movapd_a:
    """movapd"""
    MNEMONIC = 'movapd'
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
        buf.put1(0x28)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class movapd_b:
    """movapd"""
    MNEMONIC = 'movapd'
    FIELDS = ('xmm_m128', 'xmm1')

    def __init__(self, xmm_m128, xmm1):
        self.xmm_m128 = xmm_m128
        self.xmm1 = xmm1

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
        buf.put1(0x29)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class movaps_a:
    """movaps"""
    MNEMONIC = 'movaps'
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
        buf.put1(0x28)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class movaps_b:
    """movaps"""
    MNEMONIC = 'movaps'
    FIELDS = ('xmm_m128', 'xmm1')

    def __init__(self, xmm_m128, xmm1):
        self.xmm_m128 = xmm_m128
        self.xmm1 = xmm1

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
        buf.put1(0x29)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class movdqa_a:
    """movdqa"""
    MNEMONIC = 'movdqa'
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
        buf.put1(0x6f)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class movdqa_b:
    """movdqa"""
    MNEMONIC = 'movdqa'
    FIELDS = ('xmm_m128', 'xmm1')

    def __init__(self, xmm_m128, xmm1):
        self.xmm_m128 = xmm_m128
        self.xmm1 = xmm1

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
        buf.put1(0x7f)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class movupd_a:
    """movupd"""
    MNEMONIC = 'movupd'
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
        buf.put1(0x10)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class movupd_b:
    """movupd"""
    MNEMONIC = 'movupd'
    FIELDS = ('xmm_m128', 'xmm1')

    def __init__(self, xmm_m128, xmm1):
        self.xmm_m128 = xmm_m128
        self.xmm1 = xmm1

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
        buf.put1(0x11)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class movups_a:
    """movups"""
    MNEMONIC = 'movups'
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
        buf.put1(0x10)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class movups_b:
    """movups"""
    MNEMONIC = 'movups'
    FIELDS = ('xmm_m128', 'xmm1')

    def __init__(self, xmm_m128, xmm1):
        self.xmm_m128 = xmm_m128
        self.xmm1 = xmm1

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
        buf.put1(0x11)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class movdqu_a:
    """movdqu"""
    MNEMONIC = 'movdqu'
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
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m128.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x6f)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class movdqu_b:
    """movdqu"""
    MNEMONIC = 'movdqu'
    FIELDS = ('xmm_m128', 'xmm1')

    def __init__(self, xmm_m128, xmm1):
        self.xmm_m128 = xmm_m128
        self.xmm1 = xmm1

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m128.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x7f)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class mulb_m:
    """mulb"""
    MNEMONIC = 'mulb'
    FIELDS = ('ax', 'rm8')

    def __init__(self, ax, rm8):
        self.ax = ax
        self.rm8 = rm8

    def encode(self, buf):
        if isinstance(self.rm8, Mem):
            rm8 = self.rm8
            trap_code = rm8.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = True
        w_bit = False
        digit = 0x4
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf6)
        reg = 0x4
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class mulw_m:
    """mulw"""
    MNEMONIC = 'mulw'
    FIELDS = ('ax', 'dx', 'rm16')

    def __init__(self, ax, dx, rm16):
        self.ax = ax
        self.dx = dx
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
        digit = 0x4
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x4
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class mull_m:
    """mull"""
    MNEMONIC = 'mull'
    FIELDS = ('eax', 'edx', 'rm32')

    def __init__(self, eax, edx, rm32):
        self.eax = eax
        self.edx = edx
        self.rm32 = rm32

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = False
        digit = 0x4
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x4
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class mulq_m:
    """mulq"""
    MNEMONIC = 'mulq'
    FIELDS = ('rax', 'rdx', 'rm64')

    def __init__(self, rax, rdx, rm64):
        self.rax = rax
        self.rdx = rdx
        self.rm64 = rm64

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = True
        digit = 0x4
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x4
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class mulxl_rvm:
    """mulxl"""
    MNEMONIC = 'mulxl'
    FIELDS = ('r32a', 'r32b', 'rm32', 'edx')

    def __init__(self, r32a, r32b, rm32, edx):
        self.r32a = r32a
        self.r32b = r32b
        self.rm32 = rm32
        self.edx = edx

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00010
        w = False
        reg = self.r32a.enc()
        vvvv = self.r32b.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf6)
        reg = self.r32a.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class mulxq_rvm:
    """mulxq"""
    MNEMONIC = 'mulxq'
    FIELDS = ('r64a', 'r64b', 'rm64', 'rdx')

    def __init__(self, r64a, r64b, rm64, rdx):
        self.r64a = r64a
        self.r64b = r64b
        self.rm64 = rm64
        self.rdx = rdx

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00010
        w = True
        reg = self.r64a.enc()
        vvvv = self.r64b.enc()
        rm = self.rm64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf6)
        reg = self.r64a.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class mulss_a:
    """mulss"""
    MNEMONIC = 'mulss'
    FIELDS = ('xmm1', 'xmm_m32')

    def __init__(self, xmm1, xmm_m32):
        self.xmm1 = xmm1
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x59)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class mulsd_a:
    """mulsd"""
    MNEMONIC = 'mulsd'
    FIELDS = ('xmm1', 'xmm_m64')

    def __init__(self, xmm1, xmm_m64):
        self.xmm1 = xmm1
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0xF2)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x59)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class mulps_a:
    """mulps"""
    MNEMONIC = 'mulps'
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
        buf.put1(0x59)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class mulpd_a:
    """mulpd"""
    MNEMONIC = 'mulpd'
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
        buf.put1(0x59)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)
