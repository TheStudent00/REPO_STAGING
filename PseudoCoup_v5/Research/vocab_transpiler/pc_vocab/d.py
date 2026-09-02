"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class divb_m:
    """divb"""
    MNEMONIC = 'divb'
    FIELDS = ('ax', 'rm8', 'trap')

    def __init__(self, ax, rm8, trap):
        self.ax = ax
        self.rm8 = rm8
        self.trap = trap

    def encode(self, buf):
        buf.add_trap(self.trap)
        uses_8bit = True
        w_bit = False
        digit = 0x6
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf6)
        reg = 0x6
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class divw_m:
    """divw"""
    MNEMONIC = 'divw'
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
        digit = 0x6
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x6
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class divl_m:
    """divl"""
    MNEMONIC = 'divl'
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
        digit = 0x6
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x6
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class divq_m:
    """divq"""
    MNEMONIC = 'divq'
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
        digit = 0x6
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x6
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class divss_a:
    """divss"""
    MNEMONIC = 'divss'
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
        buf.put1(0x5e)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class divsd_a:
    """divsd"""
    MNEMONIC = 'divsd'
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
        buf.put1(0x5e)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class divps_a:
    """divps"""
    MNEMONIC = 'divps'
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
        buf.put1(0x5e)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class divpd_a:
    """divpd"""
    MNEMONIC = 'divpd'
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
        buf.put1(0x5e)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)
