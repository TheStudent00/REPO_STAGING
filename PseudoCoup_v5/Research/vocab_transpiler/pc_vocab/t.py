"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class tzcntw_a:
    """tzcntw"""
    MNEMONIC = 'tzcntw'
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
        buf.put1(0xbc)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class tzcntl_a:
    """tzcntl"""
    MNEMONIC = 'tzcntl'
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
        buf.put1(0xbc)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class tzcntq_a:
    """tzcntq"""
    MNEMONIC = 'tzcntq'
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
        buf.put1(0xbc)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class testb_i:
    """testb"""
    MNEMONIC = 'testb'
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
        buf.put1(0xa8)
        self.imm8.encode(buf)

class testw_i:
    """testw"""
    MNEMONIC = 'testw'
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
        buf.put1(0xa9)
        self.imm16.encode(buf)

class testl_i:
    """testl"""
    MNEMONIC = 'testl'
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
        buf.put1(0xa9)
        self.imm32.encode(buf)

class testq_i:
    """testq"""
    MNEMONIC = 'testq'
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
        buf.put1(0xa9)
        self.imm32.encode(buf)

class testb_mi:
    """testb"""
    MNEMONIC = 'testb'
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
        buf.put1(0xf6)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class testw_mi:
    """testw"""
    MNEMONIC = 'testw'
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
        buf.put1(0xf7)
        reg = 0x0
        self.rm16.encode_rex_suffixes(buf, reg, 2, None)
        self.imm16.encode(buf)

class testl_mi:
    """testl"""
    MNEMONIC = 'testl'
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
        buf.put1(0xf7)
        reg = 0x0
        self.rm32.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class testq_mi:
    """testq"""
    MNEMONIC = 'testq'
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
        buf.put1(0xf7)
        reg = 0x0
        self.rm64.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class testb_mr:
    """testb"""
    MNEMONIC = 'testb'
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
        buf.put1(0x84)
        reg = self.r8.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class testw_mr:
    """testw"""
    MNEMONIC = 'testw'
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
        buf.put1(0x85)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class testl_mr:
    """testl"""
    MNEMONIC = 'testl'
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
        buf.put1(0x85)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class testq_mr:
    """testq"""
    MNEMONIC = 'testq'
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
        buf.put1(0x85)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)
