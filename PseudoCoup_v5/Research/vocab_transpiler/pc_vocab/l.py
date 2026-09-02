"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class lock_addb_mi:
    """lock_addb_mi"""
    MNEMONIC = 'lock_addb_mi'
    FIELDS = ('m8', 'imm8')

    def __init__(self, m8, imm8):
        self.m8 = m8
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x0
        rex = self.m8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x80)
        reg = 0x0
        self.m8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_addw_mi:
    """lock_addw_mi"""
    MNEMONIC = 'lock_addw_mi'
    FIELDS = ('m16', 'imm16')

    def __init__(self, m16, imm16):
        self.m16 = m16
        self.imm16 = imm16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        digit = 0x0
        rex = self.m16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x0
        self.m16.encode_rex_suffixes(buf, reg, 2, None)
        self.imm16.encode(buf)

class lock_addl_mi:
    """lock_addl_mi"""
    MNEMONIC = 'lock_addl_mi'
    FIELDS = ('m32', 'imm32')

    def __init__(self, m32, imm32):
        self.m32 = m32
        self.imm32 = imm32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x0
        rex = self.m32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x0
        self.m32.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class lock_addq_mi_sxl:
    """lock_addq_mi_sxl"""
    MNEMONIC = 'lock_addq_mi_sxl'
    FIELDS = ('m64', 'imm32')

    def __init__(self, m64, imm32):
        self.m64 = m64
        self.imm32 = imm32

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x0
        rex = self.m64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x0
        self.m64.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class lock_addl_mi_sxb:
    """lock_addl_mi_sxb"""
    MNEMONIC = 'lock_addl_mi_sxb'
    FIELDS = ('m32', 'imm8')

    def __init__(self, m32, imm8):
        self.m32 = m32
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x0
        rex = self.m32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x0
        self.m32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_addq_mi_sxb:
    """lock_addq_mi_sxb"""
    MNEMONIC = 'lock_addq_mi_sxb'
    FIELDS = ('m64', 'imm8')

    def __init__(self, m64, imm8):
        self.m64 = m64
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x0
        rex = self.m64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x0
        self.m64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_addb_mr:
    """lock_addb_mr"""
    MNEMONIC = 'lock_addb_mr'
    FIELDS = ('m8', 'r8')

    def __init__(self, m8, r8):
        self.m8 = m8
        self.r8 = r8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = True
        w_bit = False
        reg = self.r8.enc()
        rex = self.m8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0)
        reg = self.r8.enc()
        self.m8.encode_rex_suffixes(buf, reg, 0, None)

class lock_addw_mr:
    """lock_addw_mr"""
    MNEMONIC = 'lock_addw_mr'
    FIELDS = ('m16', 'r16')

    def __init__(self, m16, r16):
        self.m16 = m16
        self.r16 = r16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.r16.enc()
        rex = self.m16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x1)
        reg = self.r16.enc()
        self.m16.encode_rex_suffixes(buf, reg, 0, None)

class lock_addl_mr:
    """lock_addl_mr"""
    MNEMONIC = 'lock_addl_mr'
    FIELDS = ('m32', 'r32')

    def __init__(self, m32, r32):
        self.m32 = m32
        self.r32 = r32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x1)
        reg = self.r32.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class lock_addq_mr:
    """lock_addq_mr"""
    MNEMONIC = 'lock_addq_mr'
    FIELDS = ('m64', 'r64')

    def __init__(self, m64, r64):
        self.m64 = m64
        self.r64 = r64

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x1)
        reg = self.r64.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class lock_adcb_mi:
    """lock_adcb_mi"""
    MNEMONIC = 'lock_adcb_mi'
    FIELDS = ('m8', 'imm8')

    def __init__(self, m8, imm8):
        self.m8 = m8
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x2
        rex = self.m8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x80)
        reg = 0x2
        self.m8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_adcw_mi:
    """lock_adcw_mi"""
    MNEMONIC = 'lock_adcw_mi'
    FIELDS = ('m16', 'imm16')

    def __init__(self, m16, imm16):
        self.m16 = m16
        self.imm16 = imm16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        digit = 0x2
        rex = self.m16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x2
        self.m16.encode_rex_suffixes(buf, reg, 2, None)
        self.imm16.encode(buf)

class lock_adcl_mi:
    """lock_adcl_mi"""
    MNEMONIC = 'lock_adcl_mi'
    FIELDS = ('m32', 'imm32')

    def __init__(self, m32, imm32):
        self.m32 = m32
        self.imm32 = imm32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x2
        rex = self.m32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x2
        self.m32.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class lock_adcq_mi_sxl:
    """lock_adcq_mi_sxl"""
    MNEMONIC = 'lock_adcq_mi_sxl'
    FIELDS = ('m64', 'imm32')

    def __init__(self, m64, imm32):
        self.m64 = m64
        self.imm32 = imm32

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x2
        rex = self.m64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x2
        self.m64.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class lock_adcl_mi_sxb:
    """lock_adcl_mi_sxb"""
    MNEMONIC = 'lock_adcl_mi_sxb'
    FIELDS = ('m32', 'imm8')

    def __init__(self, m32, imm8):
        self.m32 = m32
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x2
        rex = self.m32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x2
        self.m32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_adcq_mi_sxb:
    """lock_adcq_mi_sxb"""
    MNEMONIC = 'lock_adcq_mi_sxb'
    FIELDS = ('m64', 'imm8')

    def __init__(self, m64, imm8):
        self.m64 = m64
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x2
        rex = self.m64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x2
        self.m64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_adcb_mr:
    """lock_adcb_mr"""
    MNEMONIC = 'lock_adcb_mr'
    FIELDS = ('m8', 'r8')

    def __init__(self, m8, r8):
        self.m8 = m8
        self.r8 = r8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = True
        w_bit = False
        reg = self.r8.enc()
        rex = self.m8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x10)
        reg = self.r8.enc()
        self.m8.encode_rex_suffixes(buf, reg, 0, None)

class lock_adcw_mr:
    """lock_adcw_mr"""
    MNEMONIC = 'lock_adcw_mr'
    FIELDS = ('m16', 'r16')

    def __init__(self, m16, r16):
        self.m16 = m16
        self.r16 = r16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.r16.enc()
        rex = self.m16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x11)
        reg = self.r16.enc()
        self.m16.encode_rex_suffixes(buf, reg, 0, None)

class lock_adcl_mr:
    """lock_adcl_mr"""
    MNEMONIC = 'lock_adcl_mr'
    FIELDS = ('m32', 'r32')

    def __init__(self, m32, r32):
        self.m32 = m32
        self.r32 = r32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x11)
        reg = self.r32.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class lock_adcq_mr:
    """lock_adcq_mr"""
    MNEMONIC = 'lock_adcq_mr'
    FIELDS = ('m64', 'r64')

    def __init__(self, m64, r64):
        self.m64 = m64
        self.r64 = r64

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x11)
        reg = self.r64.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class lock_xaddb_mr:
    """lock_xaddb_mr"""
    MNEMONIC = 'lock_xaddb_mr'
    FIELDS = ('m8', 'r8')

    def __init__(self, m8, r8):
        self.m8 = m8
        self.r8 = r8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = True
        w_bit = False
        reg = self.r8.enc()
        rex = self.m8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xc0)
        reg = self.r8.enc()
        self.m8.encode_rex_suffixes(buf, reg, 0, None)

class lock_xaddw_mr:
    """lock_xaddw_mr"""
    MNEMONIC = 'lock_xaddw_mr'
    FIELDS = ('m16', 'r16')

    def __init__(self, m16, r16):
        self.m16 = m16
        self.r16 = r16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.r16.enc()
        rex = self.m16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xc1)
        reg = self.r16.enc()
        self.m16.encode_rex_suffixes(buf, reg, 0, None)

class lock_xaddl_mr:
    """lock_xaddl_mr"""
    MNEMONIC = 'lock_xaddl_mr'
    FIELDS = ('m32', 'r32')

    def __init__(self, m32, r32):
        self.m32 = m32
        self.r32 = r32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xc1)
        reg = self.r32.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class lock_xaddq_mr:
    """lock_xaddq_mr"""
    MNEMONIC = 'lock_xaddq_mr'
    FIELDS = ('m64', 'r64')

    def __init__(self, m64, r64):
        self.m64 = m64
        self.r64 = r64

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xc1)
        reg = self.r64.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class lock_andb_mi:
    """lock_andb_mi"""
    MNEMONIC = 'lock_andb_mi'
    FIELDS = ('m8', 'imm8')

    def __init__(self, m8, imm8):
        self.m8 = m8
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x4
        rex = self.m8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x80)
        reg = 0x4
        self.m8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_andw_mi:
    """lock_andw_mi"""
    MNEMONIC = 'lock_andw_mi'
    FIELDS = ('m16', 'imm16')

    def __init__(self, m16, imm16):
        self.m16 = m16
        self.imm16 = imm16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        digit = 0x4
        rex = self.m16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x4
        self.m16.encode_rex_suffixes(buf, reg, 2, None)
        self.imm16.encode(buf)

class lock_andl_mi:
    """lock_andl_mi"""
    MNEMONIC = 'lock_andl_mi'
    FIELDS = ('m32', 'imm32')

    def __init__(self, m32, imm32):
        self.m32 = m32
        self.imm32 = imm32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x4
        rex = self.m32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x4
        self.m32.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class lock_andq_mi_sxl:
    """lock_andq_mi_sxl"""
    MNEMONIC = 'lock_andq_mi_sxl'
    FIELDS = ('m64', 'imm32')

    def __init__(self, m64, imm32):
        self.m64 = m64
        self.imm32 = imm32

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x4
        rex = self.m64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x4
        self.m64.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class lock_andl_mi_sxb:
    """lock_andl_mi_sxb"""
    MNEMONIC = 'lock_andl_mi_sxb'
    FIELDS = ('m32', 'imm8')

    def __init__(self, m32, imm8):
        self.m32 = m32
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x4
        rex = self.m32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x4
        self.m32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_andq_mi_sxb:
    """lock_andq_mi_sxb"""
    MNEMONIC = 'lock_andq_mi_sxb'
    FIELDS = ('m64', 'imm8')

    def __init__(self, m64, imm8):
        self.m64 = m64
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x4
        rex = self.m64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x4
        self.m64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_andb_mr:
    """lock_andb_mr"""
    MNEMONIC = 'lock_andb_mr'
    FIELDS = ('m8', 'r8')

    def __init__(self, m8, r8):
        self.m8 = m8
        self.r8 = r8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = True
        w_bit = False
        reg = self.r8.enc()
        rex = self.m8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x20)
        reg = self.r8.enc()
        self.m8.encode_rex_suffixes(buf, reg, 0, None)

class lock_andw_mr:
    """lock_andw_mr"""
    MNEMONIC = 'lock_andw_mr'
    FIELDS = ('m16', 'r16')

    def __init__(self, m16, r16):
        self.m16 = m16
        self.r16 = r16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.r16.enc()
        rex = self.m16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x21)
        reg = self.r16.enc()
        self.m16.encode_rex_suffixes(buf, reg, 0, None)

class lock_andl_mr:
    """lock_andl_mr"""
    MNEMONIC = 'lock_andl_mr'
    FIELDS = ('m32', 'r32')

    def __init__(self, m32, r32):
        self.m32 = m32
        self.r32 = r32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x21)
        reg = self.r32.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class lock_andq_mr:
    """lock_andq_mr"""
    MNEMONIC = 'lock_andq_mr'
    FIELDS = ('m64', 'r64')

    def __init__(self, m64, r64):
        self.m64 = m64
        self.r64 = r64

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x21)
        reg = self.r64.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class lock_cmpxchg16b_m:
    """lock_cmpxchg16b_m"""
    MNEMONIC = 'lock_cmpxchg16b_m'
    FIELDS = ('rax', 'rdx', 'rbx', 'rcx', 'm128')

    def __init__(self, rax, rdx, rbx, rcx, m128):
        self.rax = rax
        self.rdx = rdx
        self.rbx = rbx
        self.rcx = rcx
        self.m128 = m128

    def encode(self, buf):
        trap_code = self.m128.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x1
        rex = self.m128.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xc7)
        reg = 0x1
        self.m128.encode_rex_suffixes(buf, reg, 0, None)

class lock_cmpxchgb_mr:
    """lock_cmpxchgb_mr"""
    MNEMONIC = 'lock_cmpxchgb_mr'
    FIELDS = ('m8', 'r8', 'al')

    def __init__(self, m8, r8, al):
        self.m8 = m8
        self.r8 = r8
        self.al = al

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = True
        w_bit = False
        reg = self.r8.enc()
        rex = self.m8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xb0)
        reg = self.r8.enc()
        self.m8.encode_rex_suffixes(buf, reg, 0, None)

class lock_cmpxchgw_mr:
    """lock_cmpxchgw_mr"""
    MNEMONIC = 'lock_cmpxchgw_mr'
    FIELDS = ('m16', 'r16', 'ax')

    def __init__(self, m16, r16, ax):
        self.m16 = m16
        self.r16 = r16
        self.ax = ax

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.r16.enc()
        rex = self.m16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xb1)
        reg = self.r16.enc()
        self.m16.encode_rex_suffixes(buf, reg, 0, None)

class lock_cmpxchgl_mr:
    """lock_cmpxchgl_mr"""
    MNEMONIC = 'lock_cmpxchgl_mr'
    FIELDS = ('m32', 'r32', 'eax')

    def __init__(self, m32, r32, eax):
        self.m32 = m32
        self.r32 = r32
        self.eax = eax

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xb1)
        reg = self.r32.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class lock_cmpxchgq_mr:
    """lock_cmpxchgq_mr"""
    MNEMONIC = 'lock_cmpxchgq_mr'
    FIELDS = ('m64', 'r64', 'rax')

    def __init__(self, m64, r64, rax):
        self.m64 = m64
        self.r64 = r64
        self.rax = rax

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xb1)
        reg = self.r64.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class lzcntw_rm:
    """lzcntw"""
    MNEMONIC = 'lzcntw'
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
        buf.put1(0xF3)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.r16.enc()
        rex = self.rm16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xbd)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class lzcntl_rm:
    """lzcntl"""
    MNEMONIC = 'lzcntl'
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
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.rm32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xbd)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class lzcntq_rm:
    """lzcntq"""
    MNEMONIC = 'lzcntq'
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
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.rm64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xbd)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class lfence_zo:
    """lfence"""
    MNEMONIC = 'lfence'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0xae)
        buf.put1(0xe8)

class leaw_rm:
    """leaw"""
    MNEMONIC = 'leaw'
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
        buf.put1(0x8d)
        reg = self.r16.enc()
        self.m16.encode_rex_suffixes(buf, reg, 0, None)

class leal_rm:
    """leal"""
    MNEMONIC = 'leal'
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
        buf.put1(0x8d)
        reg = self.r32.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class leaq_rm:
    """leaq"""
    MNEMONIC = 'leaq'
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
        buf.put1(0x8d)
        reg = self.r64.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class lock_orb_mi:
    """lock_orb_mi"""
    MNEMONIC = 'lock_orb_mi'
    FIELDS = ('m8', 'imm8')

    def __init__(self, m8, imm8):
        self.m8 = m8
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x1
        rex = self.m8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x80)
        reg = 0x1
        self.m8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_orw_mi:
    """lock_orw_mi"""
    MNEMONIC = 'lock_orw_mi'
    FIELDS = ('m16', 'imm16')

    def __init__(self, m16, imm16):
        self.m16 = m16
        self.imm16 = imm16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        digit = 0x1
        rex = self.m16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x1
        self.m16.encode_rex_suffixes(buf, reg, 2, None)
        self.imm16.encode(buf)

class lock_orl_mi:
    """lock_orl_mi"""
    MNEMONIC = 'lock_orl_mi'
    FIELDS = ('m32', 'imm32')

    def __init__(self, m32, imm32):
        self.m32 = m32
        self.imm32 = imm32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x1
        rex = self.m32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x1
        self.m32.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class lock_orq_mi_sxl:
    """lock_orq_mi_sxl"""
    MNEMONIC = 'lock_orq_mi_sxl'
    FIELDS = ('m64', 'imm32')

    def __init__(self, m64, imm32):
        self.m64 = m64
        self.imm32 = imm32

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x1
        rex = self.m64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x1
        self.m64.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class lock_orl_mi_sxb:
    """lock_orl_mi_sxb"""
    MNEMONIC = 'lock_orl_mi_sxb'
    FIELDS = ('m32', 'imm8')

    def __init__(self, m32, imm8):
        self.m32 = m32
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x1
        rex = self.m32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x1
        self.m32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_orq_mi_sxb:
    """lock_orq_mi_sxb"""
    MNEMONIC = 'lock_orq_mi_sxb'
    FIELDS = ('m64', 'imm8')

    def __init__(self, m64, imm8):
        self.m64 = m64
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x1
        rex = self.m64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x1
        self.m64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_orb_mr:
    """lock_orb_mr"""
    MNEMONIC = 'lock_orb_mr'
    FIELDS = ('m8', 'r8')

    def __init__(self, m8, r8):
        self.m8 = m8
        self.r8 = r8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = True
        w_bit = False
        reg = self.r8.enc()
        rex = self.m8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x8)
        reg = self.r8.enc()
        self.m8.encode_rex_suffixes(buf, reg, 0, None)

class lock_orw_mr:
    """lock_orw_mr"""
    MNEMONIC = 'lock_orw_mr'
    FIELDS = ('m16', 'r16')

    def __init__(self, m16, r16):
        self.m16 = m16
        self.r16 = r16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.r16.enc()
        rex = self.m16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x9)
        reg = self.r16.enc()
        self.m16.encode_rex_suffixes(buf, reg, 0, None)

class lock_orl_mr:
    """lock_orl_mr"""
    MNEMONIC = 'lock_orl_mr'
    FIELDS = ('m32', 'r32')

    def __init__(self, m32, r32):
        self.m32 = m32
        self.r32 = r32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x9)
        reg = self.r32.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class lock_orq_mr:
    """lock_orq_mr"""
    MNEMONIC = 'lock_orq_mr'
    FIELDS = ('m64', 'r64')

    def __init__(self, m64, r64):
        self.m64 = m64
        self.r64 = r64

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x9)
        reg = self.r64.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class lock_subb_mi:
    """lock_subb_mi"""
    MNEMONIC = 'lock_subb_mi'
    FIELDS = ('m8', 'imm8')

    def __init__(self, m8, imm8):
        self.m8 = m8
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x5
        rex = self.m8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x80)
        reg = 0x5
        self.m8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_subw_mi:
    """lock_subw_mi"""
    MNEMONIC = 'lock_subw_mi'
    FIELDS = ('m16', 'imm16')

    def __init__(self, m16, imm16):
        self.m16 = m16
        self.imm16 = imm16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        digit = 0x5
        rex = self.m16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x5
        self.m16.encode_rex_suffixes(buf, reg, 2, None)
        self.imm16.encode(buf)

class lock_subl_mi:
    """lock_subl_mi"""
    MNEMONIC = 'lock_subl_mi'
    FIELDS = ('m32', 'imm32')

    def __init__(self, m32, imm32):
        self.m32 = m32
        self.imm32 = imm32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x5
        rex = self.m32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x5
        self.m32.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class lock_subq_mi_sxl:
    """lock_subq_mi_sxl"""
    MNEMONIC = 'lock_subq_mi_sxl'
    FIELDS = ('m64', 'imm32')

    def __init__(self, m64, imm32):
        self.m64 = m64
        self.imm32 = imm32

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x5
        rex = self.m64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x5
        self.m64.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class lock_subl_mi_sxb:
    """lock_subl_mi_sxb"""
    MNEMONIC = 'lock_subl_mi_sxb'
    FIELDS = ('m32', 'imm8')

    def __init__(self, m32, imm8):
        self.m32 = m32
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x5
        rex = self.m32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x5
        self.m32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_subq_mi_sxb:
    """lock_subq_mi_sxb"""
    MNEMONIC = 'lock_subq_mi_sxb'
    FIELDS = ('m64', 'imm8')

    def __init__(self, m64, imm8):
        self.m64 = m64
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x5
        rex = self.m64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x5
        self.m64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_subb_mr:
    """lock_subb_mr"""
    MNEMONIC = 'lock_subb_mr'
    FIELDS = ('m8', 'r8')

    def __init__(self, m8, r8):
        self.m8 = m8
        self.r8 = r8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = True
        w_bit = False
        reg = self.r8.enc()
        rex = self.m8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x28)
        reg = self.r8.enc()
        self.m8.encode_rex_suffixes(buf, reg, 0, None)

class lock_subw_mr:
    """lock_subw_mr"""
    MNEMONIC = 'lock_subw_mr'
    FIELDS = ('m16', 'r16')

    def __init__(self, m16, r16):
        self.m16 = m16
        self.r16 = r16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.r16.enc()
        rex = self.m16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x29)
        reg = self.r16.enc()
        self.m16.encode_rex_suffixes(buf, reg, 0, None)

class lock_subl_mr:
    """lock_subl_mr"""
    MNEMONIC = 'lock_subl_mr'
    FIELDS = ('m32', 'r32')

    def __init__(self, m32, r32):
        self.m32 = m32
        self.r32 = r32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x29)
        reg = self.r32.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class lock_subq_mr:
    """lock_subq_mr"""
    MNEMONIC = 'lock_subq_mr'
    FIELDS = ('m64', 'r64')

    def __init__(self, m64, r64):
        self.m64 = m64
        self.r64 = r64

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x29)
        reg = self.r64.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class lock_sbbb_mi:
    """lock_sbbb_mi"""
    MNEMONIC = 'lock_sbbb_mi'
    FIELDS = ('m8', 'imm8')

    def __init__(self, m8, imm8):
        self.m8 = m8
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x3
        rex = self.m8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x80)
        reg = 0x3
        self.m8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_sbbw_mi:
    """lock_sbbw_mi"""
    MNEMONIC = 'lock_sbbw_mi'
    FIELDS = ('m16', 'imm16')

    def __init__(self, m16, imm16):
        self.m16 = m16
        self.imm16 = imm16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        digit = 0x3
        rex = self.m16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x3
        self.m16.encode_rex_suffixes(buf, reg, 2, None)
        self.imm16.encode(buf)

class lock_sbbl_mi:
    """lock_sbbl_mi"""
    MNEMONIC = 'lock_sbbl_mi'
    FIELDS = ('m32', 'imm32')

    def __init__(self, m32, imm32):
        self.m32 = m32
        self.imm32 = imm32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x3
        rex = self.m32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x3
        self.m32.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class lock_sbbq_mi_sxl:
    """lock_sbbq_mi_sxl"""
    MNEMONIC = 'lock_sbbq_mi_sxl'
    FIELDS = ('m64', 'imm32')

    def __init__(self, m64, imm32):
        self.m64 = m64
        self.imm32 = imm32

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x3
        rex = self.m64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x3
        self.m64.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class lock_sbbl_mi_sxb:
    """lock_sbbl_mi_sxb"""
    MNEMONIC = 'lock_sbbl_mi_sxb'
    FIELDS = ('m32', 'imm8')

    def __init__(self, m32, imm8):
        self.m32 = m32
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x3
        rex = self.m32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x3
        self.m32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_sbbq_mi_sxb:
    """lock_sbbq_mi_sxb"""
    MNEMONIC = 'lock_sbbq_mi_sxb'
    FIELDS = ('m64', 'imm8')

    def __init__(self, m64, imm8):
        self.m64 = m64
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x3
        rex = self.m64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x3
        self.m64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_sbbb_mr:
    """lock_sbbb_mr"""
    MNEMONIC = 'lock_sbbb_mr'
    FIELDS = ('m8', 'r8')

    def __init__(self, m8, r8):
        self.m8 = m8
        self.r8 = r8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = True
        w_bit = False
        reg = self.r8.enc()
        rex = self.m8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x18)
        reg = self.r8.enc()
        self.m8.encode_rex_suffixes(buf, reg, 0, None)

class lock_sbbw_mr:
    """lock_sbbw_mr"""
    MNEMONIC = 'lock_sbbw_mr'
    FIELDS = ('m16', 'r16')

    def __init__(self, m16, r16):
        self.m16 = m16
        self.r16 = r16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.r16.enc()
        rex = self.m16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x19)
        reg = self.r16.enc()
        self.m16.encode_rex_suffixes(buf, reg, 0, None)

class lock_sbbl_mr:
    """lock_sbbl_mr"""
    MNEMONIC = 'lock_sbbl_mr'
    FIELDS = ('m32', 'r32')

    def __init__(self, m32, r32):
        self.m32 = m32
        self.r32 = r32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x19)
        reg = self.r32.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class lock_sbbq_mr:
    """lock_sbbq_mr"""
    MNEMONIC = 'lock_sbbq_mr'
    FIELDS = ('m64', 'r64')

    def __init__(self, m64, r64):
        self.m64 = m64
        self.r64 = r64

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x19)
        reg = self.r64.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class lock_xorb_mi:
    """lock_xorb_mi"""
    MNEMONIC = 'lock_xorb_mi'
    FIELDS = ('m8', 'imm8')

    def __init__(self, m8, imm8):
        self.m8 = m8
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x6
        rex = self.m8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x80)
        reg = 0x6
        self.m8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_xorw_mi:
    """lock_xorw_mi"""
    MNEMONIC = 'lock_xorw_mi'
    FIELDS = ('m16', 'imm16')

    def __init__(self, m16, imm16):
        self.m16 = m16
        self.imm16 = imm16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        digit = 0x6
        rex = self.m16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x6
        self.m16.encode_rex_suffixes(buf, reg, 2, None)
        self.imm16.encode(buf)

class lock_xorl_mi:
    """lock_xorl_mi"""
    MNEMONIC = 'lock_xorl_mi'
    FIELDS = ('m32', 'imm32')

    def __init__(self, m32, imm32):
        self.m32 = m32
        self.imm32 = imm32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x6
        rex = self.m32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x6
        self.m32.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class lock_xorq_mi_sxl:
    """lock_xorq_mi_sxl"""
    MNEMONIC = 'lock_xorq_mi_sxl'
    FIELDS = ('m64', 'imm32')

    def __init__(self, m64, imm32):
        self.m64 = m64
        self.imm32 = imm32

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x6
        rex = self.m64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x6
        self.m64.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class lock_xorl_mi_sxb:
    """lock_xorl_mi_sxb"""
    MNEMONIC = 'lock_xorl_mi_sxb'
    FIELDS = ('m32', 'imm8')

    def __init__(self, m32, imm8):
        self.m32 = m32
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        digit = 0x6
        rex = self.m32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x6
        self.m32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_xorq_mi_sxb:
    """lock_xorq_mi_sxb"""
    MNEMONIC = 'lock_xorq_mi_sxb'
    FIELDS = ('m64', 'imm8')

    def __init__(self, m64, imm8):
        self.m64 = m64
        self.imm8 = imm8

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        digit = 0x6
        rex = self.m64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x6
        self.m64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class lock_xorb_mr:
    """lock_xorb_mr"""
    MNEMONIC = 'lock_xorb_mr'
    FIELDS = ('m8', 'r8')

    def __init__(self, m8, r8):
        self.m8 = m8
        self.r8 = r8

    def encode(self, buf):
        trap_code = self.m8.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = True
        w_bit = False
        reg = self.r8.enc()
        rex = self.m8.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x30)
        reg = self.r8.enc()
        self.m8.encode_rex_suffixes(buf, reg, 0, None)

class lock_xorw_mr:
    """lock_xorw_mr"""
    MNEMONIC = 'lock_xorw_mr'
    FIELDS = ('m16', 'r16')

    def __init__(self, m16, r16):
        self.m16 = m16
        self.r16 = r16

    def encode(self, buf):
        trap_code = self.m16.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.r16.enc()
        rex = self.m16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x31)
        reg = self.r16.enc()
        self.m16.encode_rex_suffixes(buf, reg, 0, None)

class lock_xorl_mr:
    """lock_xorl_mr"""
    MNEMONIC = 'lock_xorl_mr'
    FIELDS = ('m32', 'r32')

    def __init__(self, m32, r32):
        self.m32 = m32
        self.r32 = r32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x31)
        reg = self.r32.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class lock_xorq_mr:
    """lock_xorq_mr"""
    MNEMONIC = 'lock_xorq_mr'
    FIELDS = ('m64', 'r64')

    def __init__(self, m64, r64):
        self.m64 = m64
        self.r64 = r64

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        buf.put1(0xF0)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x31)
        reg = self.r64.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)
