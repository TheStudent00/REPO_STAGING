"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class retq_zo:
    """retq"""
    MNEMONIC = 'retq'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        buf.put1(0xc3)

class retq_i:
    """retq"""
    MNEMONIC = 'retq'
    FIELDS = ('imm16',)

    def __init__(self, imm16):
        self.imm16 = imm16

    def encode(self, buf):
        buf.put1(0xc2)
        self.imm16.encode(buf)

class rcpps_rm:
    """rcpps"""
    MNEMONIC = 'rcpps'
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
        buf.put1(0x53)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class rcpss_rm:
    """rcpss"""
    MNEMONIC = 'rcpss'
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
        buf.put1(0x53)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class rsqrtps_rm:
    """rsqrtps"""
    MNEMONIC = 'rsqrtps'
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
        buf.put1(0x52)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class rsqrtss_rm:
    """rsqrtss"""
    MNEMONIC = 'rsqrtss'
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
        buf.put1(0x52)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class roundpd_rmi:
    """roundpd"""
    MNEMONIC = 'roundpd'
    FIELDS = ('xmm1', 'xmm_m128', 'imm8')

    def __init__(self, xmm1, xmm_m128, imm8):
        self.xmm1 = xmm1
        self.xmm_m128 = xmm_m128
        self.imm8 = imm8

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
        buf.put1(0x3a)
        buf.put1(0x9)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class roundps_rmi:
    """roundps"""
    MNEMONIC = 'roundps'
    FIELDS = ('xmm1', 'xmm_m128', 'imm8')

    def __init__(self, xmm1, xmm_m128, imm8):
        self.xmm1 = xmm1
        self.xmm_m128 = xmm_m128
        self.imm8 = imm8

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
        buf.put1(0x3a)
        buf.put1(0x8)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class roundsd_rmi:
    """roundsd"""
    MNEMONIC = 'roundsd'
    FIELDS = ('xmm1', 'xmm_m64', 'imm8')

    def __init__(self, xmm1, xmm_m64, imm8):
        self.xmm1 = xmm1
        self.xmm_m64 = xmm_m64
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x3a)
        buf.put1(0xb)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class roundss_rmi:
    """roundss"""
    MNEMONIC = 'roundss'
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
        buf.put1(0xa)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class rolb_mc:
    """rolb"""
    MNEMONIC = 'rolb'
    FIELDS = ('rm8', 'cl')

    def __init__(self, rm8, cl):
        self.rm8 = rm8
        self.cl = cl

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
        buf.put1(0xd2)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class rolb_mi:
    """rolb"""
    MNEMONIC = 'rolb'
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
        buf.put1(0xc0)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class rolb_m1:
    """rolb"""
    MNEMONIC = 'rolb'
    FIELDS = ('rm8',)

    def __init__(self, rm8):
        self.rm8 = rm8

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
        buf.put1(0xd0)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class rolw_mc:
    """rolw"""
    MNEMONIC = 'rolw'
    FIELDS = ('rm16', 'cl')

    def __init__(self, rm16, cl):
        self.rm16 = rm16
        self.cl = cl

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
        buf.put1(0xd3)
        reg = 0x0
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class rolw_mi:
    """rolw"""
    MNEMONIC = 'rolw'
    FIELDS = ('rm16', 'imm8')

    def __init__(self, rm16, imm8):
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
        digit = 0x0
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x0
        self.rm16.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class rolw_m1:
    """rolw"""
    MNEMONIC = 'rolw'
    FIELDS = ('rm16',)

    def __init__(self, rm16):
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
        digit = 0x0
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd1)
        reg = 0x0
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class roll_mc:
    """roll"""
    MNEMONIC = 'roll'
    FIELDS = ('rm32', 'cl')

    def __init__(self, rm32, cl):
        self.rm32 = rm32
        self.cl = cl

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
        buf.put1(0xd3)
        reg = 0x0
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class roll_mi:
    """roll"""
    MNEMONIC = 'roll'
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
        digit = 0x0
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x0
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class roll_m1:
    """roll"""
    MNEMONIC = 'roll'
    FIELDS = ('rm32',)

    def __init__(self, rm32):
        self.rm32 = rm32

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
        buf.put1(0xd1)
        reg = 0x0
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class rolq_mc:
    """rolq"""
    MNEMONIC = 'rolq'
    FIELDS = ('rm64', 'cl')

    def __init__(self, rm64, cl):
        self.rm64 = rm64
        self.cl = cl

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
        buf.put1(0xd3)
        reg = 0x0
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class rolq_mi:
    """rolq"""
    MNEMONIC = 'rolq'
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
        digit = 0x0
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x0
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class rolq_m1:
    """rolq"""
    MNEMONIC = 'rolq'
    FIELDS = ('rm64',)

    def __init__(self, rm64):
        self.rm64 = rm64

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
        buf.put1(0xd1)
        reg = 0x0
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class rorb_mc:
    """rorb"""
    MNEMONIC = 'rorb'
    FIELDS = ('rm8', 'cl')

    def __init__(self, rm8, cl):
        self.rm8 = rm8
        self.cl = cl

    def encode(self, buf):
        if isinstance(self.rm8, Mem):
            rm8 = self.rm8
            trap_code = rm8.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = True
        w_bit = False
        digit = 0x1
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd2)
        reg = 0x1
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class rorb_mi:
    """rorb"""
    MNEMONIC = 'rorb'
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
        digit = 0x1
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc0)
        reg = 0x1
        self.rm8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class rorb_m1:
    """rorb"""
    MNEMONIC = 'rorb'
    FIELDS = ('rm8',)

    def __init__(self, rm8):
        self.rm8 = rm8

    def encode(self, buf):
        if isinstance(self.rm8, Mem):
            rm8 = self.rm8
            trap_code = rm8.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = True
        w_bit = False
        digit = 0x1
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd0)
        reg = 0x1
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class rorw_mc:
    """rorw"""
    MNEMONIC = 'rorw'
    FIELDS = ('rm16', 'cl')

    def __init__(self, rm16, cl):
        self.rm16 = rm16
        self.cl = cl

    def encode(self, buf):
        if isinstance(self.rm16, Mem):
            rm16 = self.rm16
            trap_code = rm16.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        digit = 0x1
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd3)
        reg = 0x1
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class rorw_mi:
    """rorw"""
    MNEMONIC = 'rorw'
    FIELDS = ('rm16', 'imm8')

    def __init__(self, rm16, imm8):
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
        digit = 0x1
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x1
        self.rm16.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class rorw_m1:
    """rorw"""
    MNEMONIC = 'rorw'
    FIELDS = ('rm16',)

    def __init__(self, rm16):
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
        digit = 0x1
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd1)
        reg = 0x1
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class rorl_mc:
    """rorl"""
    MNEMONIC = 'rorl'
    FIELDS = ('rm32', 'cl')

    def __init__(self, rm32, cl):
        self.rm32 = rm32
        self.cl = cl

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = False
        digit = 0x1
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd3)
        reg = 0x1
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class rorl_mi:
    """rorl"""
    MNEMONIC = 'rorl'
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
        digit = 0x1
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x1
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class rorl_m1:
    """rorl"""
    MNEMONIC = 'rorl'
    FIELDS = ('rm32',)

    def __init__(self, rm32):
        self.rm32 = rm32

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = False
        digit = 0x1
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd1)
        reg = 0x1
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class rorq_mc:
    """rorq"""
    MNEMONIC = 'rorq'
    FIELDS = ('rm64', 'cl')

    def __init__(self, rm64, cl):
        self.rm64 = rm64
        self.cl = cl

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = True
        digit = 0x1
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd3)
        reg = 0x1
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class rorq_mi:
    """rorq"""
    MNEMONIC = 'rorq'
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
        digit = 0x1
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x1
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class rorq_m1:
    """rorq"""
    MNEMONIC = 'rorq'
    FIELDS = ('rm64',)

    def __init__(self, rm64):
        self.rm64 = rm64

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = True
        digit = 0x1
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd1)
        reg = 0x1
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class rorxl_rmi:
    """rorxl"""
    MNEMONIC = 'rorxl'
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
        len = 0b0
        pp = 0b11
        mmmmm = 0b00011
        w = False
        reg = self.r32.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf0)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class rorxq_rmi:
    """rorxq"""
    MNEMONIC = 'rorxq'
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
        len = 0b0
        pp = 0b11
        mmmmm = 0b00011
        w = True
        reg = self.r64.enc()
        rm = self.rm64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf0)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)
