"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class idivb_m:
    """idivb"""
    MNEMONIC = 'idivb'
    FIELDS = ('ax', 'rm8', 'trap')

    def __init__(self, ax, rm8, trap):
        self.ax = ax
        self.rm8 = rm8
        self.trap = trap

    def encode(self, buf):
        buf.add_trap(self.trap)
        uses_8bit = True
        w_bit = False
        digit = 0x7
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf6)
        reg = 0x7
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class idivw_m:
    """idivw"""
    MNEMONIC = 'idivw'
    FIELDS = ('ax', 'dx', 'rm16', 'trap')

    def __init__(self, ax, dx, rm16, trap):
        self.ax = ax
        self.dx = dx
        self.rm16 = rm16
        self.trap = trap

    def encode(self, buf):
        buf.add_trap(self.trap)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        digit = 0x7
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x7
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class idivl_m:
    """idivl"""
    MNEMONIC = 'idivl'
    FIELDS = ('eax', 'edx', 'rm32', 'trap')

    def __init__(self, eax, edx, rm32, trap):
        self.eax = eax
        self.edx = edx
        self.rm32 = rm32
        self.trap = trap

    def encode(self, buf):
        buf.add_trap(self.trap)
        uses_8bit = False
        w_bit = False
        digit = 0x7
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x7
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class idivq_m:
    """idivq"""
    MNEMONIC = 'idivq'
    FIELDS = ('rax', 'rdx', 'rm64', 'trap')

    def __init__(self, rax, rdx, rm64, trap):
        self.rax = rax
        self.rdx = rdx
        self.rm64 = rm64
        self.trap = trap

    def encode(self, buf):
        buf.add_trap(self.trap)
        uses_8bit = False
        w_bit = True
        digit = 0x7
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x7
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class insertps_a:
    """insertps"""
    MNEMONIC = 'insertps'
    FIELDS = ('xmm1', 'xmm_m32', 'imm8')

    def __init__(self, xmm1, xmm_m32, imm8):
        self.xmm1 = xmm1
        self.xmm_m32 = xmm_m32
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x3a)
        buf.put1(0x21)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class int3_zo:
    """int3"""
    MNEMONIC = 'int3'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        buf.put1(0xcc)

class imulb_m:
    """imulb"""
    MNEMONIC = 'imulb'
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
        digit = 0x5
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf6)
        reg = 0x5
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class imulw_m:
    """imulw"""
    MNEMONIC = 'imulw'
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
        digit = 0x5
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x5
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class imull_m:
    """imull"""
    MNEMONIC = 'imull'
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
        digit = 0x5
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x5
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class imulq_m:
    """imulq"""
    MNEMONIC = 'imulq'
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
        digit = 0x5
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x5
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class imulw_rm:
    """imulw"""
    MNEMONIC = 'imulw'
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
        buf.put1(0xaf)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class imull_rm:
    """imull"""
    MNEMONIC = 'imull'
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
        buf.put1(0x0f)
        buf.put1(0xaf)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class imulq_rm:
    """imulq"""
    MNEMONIC = 'imulq'
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
        buf.put1(0x0f)
        buf.put1(0xaf)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class imulw_rmi_sxb:
    """imulw"""
    MNEMONIC = 'imulw'
    FIELDS = ('r16', 'rm16', 'imm8')

    def __init__(self, r16, rm16, imm8):
        self.r16 = r16
        self.rm16 = rm16
        self.imm8 = imm8

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
        buf.put1(0x6b)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class imull_rmi_sxb:
    """imull"""
    MNEMONIC = 'imull'
    FIELDS = ('r32', 'rm32', 'imm8')

    def __init__(self, r32, rm32, imm8):
        self.r32 = r32
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
        reg = self.r32.enc()
        rex = self.rm32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x6b)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class imulq_rmi_sxb:
    """imulq"""
    MNEMONIC = 'imulq'
    FIELDS = ('r64', 'rm64', 'imm8')

    def __init__(self, r64, rm64, imm8):
        self.r64 = r64
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
        reg = self.r64.enc()
        rex = self.rm64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x6b)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class imulw_rmi:
    """imulw"""
    MNEMONIC = 'imulw'
    FIELDS = ('r16', 'rm16', 'imm16')

    def __init__(self, r16, rm16, imm16):
        self.r16 = r16
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
        reg = self.r16.enc()
        rex = self.rm16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x69)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 2, None)
        self.imm16.encode(buf)

class imull_rmi:
    """imull"""
    MNEMONIC = 'imull'
    FIELDS = ('r32', 'rm32', 'imm32')

    def __init__(self, r32, rm32, imm32):
        self.r32 = r32
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
        reg = self.r32.enc()
        rex = self.rm32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x69)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class imulq_rmi_sxl:
    """imulq"""
    MNEMONIC = 'imulq'
    FIELDS = ('r64', 'rm64', 'imm32')

    def __init__(self, r64, rm64, imm32):
        self.r64 = r64
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
        reg = self.r64.enc()
        rex = self.rm64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x69)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)
