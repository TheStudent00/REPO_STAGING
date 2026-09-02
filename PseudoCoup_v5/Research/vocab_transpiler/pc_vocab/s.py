"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class shufpd_a:
    """shufpd"""
    MNEMONIC = 'shufpd'
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
        buf.put1(0xc6)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class shufps_a:
    """shufps"""
    MNEMONIC = 'shufps'
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
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m128.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xc6)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class sfence_zo:
    """sfence"""
    MNEMONIC = 'sfence'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0xae)
        buf.put1(0xf8)

class seta_m:
    """seta"""
    MNEMONIC = 'seta'
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
        buf.put1(0x0f)
        buf.put1(0x97)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class setae_m:
    """setae"""
    MNEMONIC = 'setae'
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
        buf.put1(0x0f)
        buf.put1(0x93)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class setb_m:
    """setb"""
    MNEMONIC = 'setb'
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
        buf.put1(0x0f)
        buf.put1(0x92)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class setbe_m:
    """setbe"""
    MNEMONIC = 'setbe'
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
        buf.put1(0x0f)
        buf.put1(0x96)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class sete_m:
    """sete"""
    MNEMONIC = 'sete'
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
        buf.put1(0x0f)
        buf.put1(0x94)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class setg_m:
    """setg"""
    MNEMONIC = 'setg'
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
        buf.put1(0x0f)
        buf.put1(0x9f)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class setge_m:
    """setge"""
    MNEMONIC = 'setge'
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
        buf.put1(0x0f)
        buf.put1(0x9d)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class setl_m:
    """setl"""
    MNEMONIC = 'setl'
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
        buf.put1(0x0f)
        buf.put1(0x9c)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class setle_m:
    """setle"""
    MNEMONIC = 'setle'
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
        buf.put1(0x0f)
        buf.put1(0x9e)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class setne_m:
    """setne"""
    MNEMONIC = 'setne'
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
        buf.put1(0x0f)
        buf.put1(0x95)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class setno_m:
    """setno"""
    MNEMONIC = 'setno'
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
        buf.put1(0x0f)
        buf.put1(0x91)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class setnp_m:
    """setnp"""
    MNEMONIC = 'setnp'
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
        buf.put1(0x0f)
        buf.put1(0x9b)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class setns_m:
    """setns"""
    MNEMONIC = 'setns'
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
        buf.put1(0x0f)
        buf.put1(0x99)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class seto_m:
    """seto"""
    MNEMONIC = 'seto'
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
        buf.put1(0x0f)
        buf.put1(0x90)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class setp_m:
    """setp"""
    MNEMONIC = 'setp'
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
        buf.put1(0x0f)
        buf.put1(0x9a)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class sets_m:
    """sets"""
    MNEMONIC = 'sets'
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
        buf.put1(0x0f)
        buf.put1(0x98)
        reg = 0x0
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class sarb_mc:
    """sarb"""
    MNEMONIC = 'sarb'
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
        digit = 0x7
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd2)
        reg = 0x7
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class sarb_mi:
    """sarb"""
    MNEMONIC = 'sarb'
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
        digit = 0x7
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc0)
        reg = 0x7
        self.rm8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class sarb_m1:
    """sarb"""
    MNEMONIC = 'sarb'
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
        digit = 0x7
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd0)
        reg = 0x7
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class sarw_mc:
    """sarw"""
    MNEMONIC = 'sarw'
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
        digit = 0x7
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd3)
        reg = 0x7
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class sarw_mi:
    """sarw"""
    MNEMONIC = 'sarw'
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
        digit = 0x7
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x7
        self.rm16.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class sarw_m1:
    """sarw"""
    MNEMONIC = 'sarw'
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
        digit = 0x7
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd1)
        reg = 0x7
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class sarl_mc:
    """sarl"""
    MNEMONIC = 'sarl'
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
        digit = 0x7
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd3)
        reg = 0x7
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class sarl_mi:
    """sarl"""
    MNEMONIC = 'sarl'
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
        digit = 0x7
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x7
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class sarl_m1:
    """sarl"""
    MNEMONIC = 'sarl'
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
        digit = 0x7
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd1)
        reg = 0x7
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class sarq_mc:
    """sarq"""
    MNEMONIC = 'sarq'
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
        digit = 0x7
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd3)
        reg = 0x7
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class sarq_mi:
    """sarq"""
    MNEMONIC = 'sarq'
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
        digit = 0x7
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x7
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class sarq_m1:
    """sarq"""
    MNEMONIC = 'sarq'
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
        digit = 0x7
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd1)
        reg = 0x7
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class shlb_mc:
    """shlb"""
    MNEMONIC = 'shlb'
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
        digit = 0x4
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd2)
        reg = 0x4
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class shlb_mi:
    """shlb"""
    MNEMONIC = 'shlb'
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
        digit = 0x4
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc0)
        reg = 0x4
        self.rm8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class shlb_m1:
    """shlb"""
    MNEMONIC = 'shlb'
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
        digit = 0x4
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd0)
        reg = 0x4
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class shlw_mc:
    """shlw"""
    MNEMONIC = 'shlw'
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
        digit = 0x4
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd3)
        reg = 0x4
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class shlw_mi:
    """shlw"""
    MNEMONIC = 'shlw'
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
        digit = 0x4
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x4
        self.rm16.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class shlw_m1:
    """shlw"""
    MNEMONIC = 'shlw'
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
        digit = 0x4
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd1)
        reg = 0x4
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class shll_mc:
    """shll"""
    MNEMONIC = 'shll'
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
        digit = 0x4
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd3)
        reg = 0x4
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class shll_mi:
    """shll"""
    MNEMONIC = 'shll'
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
        digit = 0x4
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x4
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class shll_m1:
    """shll"""
    MNEMONIC = 'shll'
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
        digit = 0x4
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd1)
        reg = 0x4
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class shlq_mc:
    """shlq"""
    MNEMONIC = 'shlq'
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
        digit = 0x4
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd3)
        reg = 0x4
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class shlq_mi:
    """shlq"""
    MNEMONIC = 'shlq'
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
        digit = 0x4
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x4
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class shlq_m1:
    """shlq"""
    MNEMONIC = 'shlq'
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
        digit = 0x4
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd1)
        reg = 0x4
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class shrb_mc:
    """shrb"""
    MNEMONIC = 'shrb'
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
        digit = 0x5
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd2)
        reg = 0x5
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class shrb_mi:
    """shrb"""
    MNEMONIC = 'shrb'
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
        digit = 0x5
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc0)
        reg = 0x5
        self.rm8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class shrb_m1:
    """shrb"""
    MNEMONIC = 'shrb'
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
        digit = 0x5
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd0)
        reg = 0x5
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class shrw_mc:
    """shrw"""
    MNEMONIC = 'shrw'
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
        digit = 0x5
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd3)
        reg = 0x5
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class shrw_mi:
    """shrw"""
    MNEMONIC = 'shrw'
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
        digit = 0x5
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x5
        self.rm16.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class shrw_m1:
    """shrw"""
    MNEMONIC = 'shrw'
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
        digit = 0x5
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd1)
        reg = 0x5
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class shrl_mc:
    """shrl"""
    MNEMONIC = 'shrl'
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
        digit = 0x5
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd3)
        reg = 0x5
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class shrl_mi:
    """shrl"""
    MNEMONIC = 'shrl'
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
        digit = 0x5
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x5
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class shrl_m1:
    """shrl"""
    MNEMONIC = 'shrl'
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
        digit = 0x5
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd1)
        reg = 0x5
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class shrq_mc:
    """shrq"""
    MNEMONIC = 'shrq'
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
        digit = 0x5
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd3)
        reg = 0x5
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class shrq_mi:
    """shrq"""
    MNEMONIC = 'shrq'
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
        digit = 0x5
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xc1)
        reg = 0x5
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class shrq_m1:
    """shrq"""
    MNEMONIC = 'shrq'
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
        digit = 0x5
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xd1)
        reg = 0x5
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class shldw_mri:
    """shldw"""
    MNEMONIC = 'shldw'
    FIELDS = ('rm16', 'r16', 'imm8')

    def __init__(self, rm16, r16, imm8):
        self.rm16 = rm16
        self.r16 = r16
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
        buf.put1(0x0f)
        buf.put1(0xa4)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class shldw_mrc:
    """shldw"""
    MNEMONIC = 'shldw'
    FIELDS = ('rm16', 'r16', 'cl')

    def __init__(self, rm16, r16, cl):
        self.rm16 = rm16
        self.r16 = r16
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
        reg = self.r16.enc()
        rex = self.rm16.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xa5)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class shldl_mri:
    """shldl"""
    MNEMONIC = 'shldl'
    FIELDS = ('rm32', 'r32', 'imm8')

    def __init__(self, rm32, r32, imm8):
        self.rm32 = rm32
        self.r32 = r32
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
        buf.put1(0x0f)
        buf.put1(0xa4)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class shldq_mri:
    """shldq"""
    MNEMONIC = 'shldq'
    FIELDS = ('rm64', 'r64', 'imm8')

    def __init__(self, rm64, r64, imm8):
        self.rm64 = rm64
        self.r64 = r64
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
        buf.put1(0x0f)
        buf.put1(0xa4)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class shldl_mrc:
    """shldl"""
    MNEMONIC = 'shldl'
    FIELDS = ('rm32', 'r32', 'cl')

    def __init__(self, rm32, r32, cl):
        self.rm32 = rm32
        self.r32 = r32
        self.cl = cl

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
        buf.put1(0xa5)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class shldq_mrc:
    """shldq"""
    MNEMONIC = 'shldq'
    FIELDS = ('rm64', 'r64', 'cl')

    def __init__(self, rm64, r64, cl):
        self.rm64 = rm64
        self.r64 = r64
        self.cl = cl

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
        buf.put1(0xa5)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class sarxl_rmv:
    """sarxl"""
    MNEMONIC = 'sarxl'
    FIELDS = ('r32a', 'rm32', 'r32b')

    def __init__(self, r32a, rm32, r32b):
        self.r32a = r32a
        self.rm32 = rm32
        self.r32b = r32b

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00010
        w = False
        reg = self.r32a.enc()
        vvvv = self.r32b.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf7)
        reg = self.r32a.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class shlxl_rmv:
    """shlxl"""
    MNEMONIC = 'shlxl'
    FIELDS = ('r32a', 'rm32', 'r32b')

    def __init__(self, r32a, rm32, r32b):
        self.r32a = r32a
        self.rm32 = rm32
        self.r32b = r32b

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.r32a.enc()
        vvvv = self.r32b.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf7)
        reg = self.r32a.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class shrxl_rmv:
    """shrxl"""
    MNEMONIC = 'shrxl'
    FIELDS = ('r32a', 'rm32', 'r32b')

    def __init__(self, r32a, rm32, r32b):
        self.r32a = r32a
        self.rm32 = rm32
        self.r32b = r32b

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
        buf.put1(0xf7)
        reg = self.r32a.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class sarxq_rmv:
    """sarxq"""
    MNEMONIC = 'sarxq'
    FIELDS = ('r64a', 'rm64', 'r64b')

    def __init__(self, r64a, rm64, r64b):
        self.r64a = r64a
        self.rm64 = rm64
        self.r64b = r64b

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00010
        w = True
        reg = self.r64a.enc()
        vvvv = self.r64b.enc()
        rm = self.rm64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf7)
        reg = self.r64a.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class shlxq_rmv:
    """shlxq"""
    MNEMONIC = 'shlxq'
    FIELDS = ('r64a', 'rm64', 'r64b')

    def __init__(self, r64a, rm64, r64b):
        self.r64a = r64a
        self.rm64 = rm64
        self.r64b = r64b

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.r64a.enc()
        vvvv = self.r64b.enc()
        rm = self.rm64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf7)
        reg = self.r64a.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class shrxq_rmv:
    """shrxq"""
    MNEMONIC = 'shrxq'
    FIELDS = ('r64a', 'rm64', 'r64b')

    def __init__(self, r64a, rm64, r64b):
        self.r64a = r64a
        self.rm64 = rm64
        self.r64b = r64b

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
        buf.put1(0xf7)
        reg = self.r64a.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class sqrtss_a:
    """sqrtss"""
    MNEMONIC = 'sqrtss'
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
        buf.put1(0x51)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class sqrtsd_a:
    """sqrtsd"""
    MNEMONIC = 'sqrtsd'
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
        buf.put1(0x51)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class sqrtps_a:
    """sqrtps"""
    MNEMONIC = 'sqrtps'
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
        buf.put1(0x51)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class sqrtpd_a:
    """sqrtpd"""
    MNEMONIC = 'sqrtpd'
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
        buf.put1(0x51)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class subb_i:
    """subb"""
    MNEMONIC = 'subb'
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
        buf.put1(0x2c)
        self.imm8.encode(buf)

class subw_i:
    """subw"""
    MNEMONIC = 'subw'
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
        buf.put1(0x2d)
        self.imm16.encode(buf)

class subl_i:
    """subl"""
    MNEMONIC = 'subl'
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
        buf.put1(0x2d)
        self.imm32.encode(buf)

class subq_i_sxl:
    """subq"""
    MNEMONIC = 'subq'
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
        buf.put1(0x2d)
        self.imm32.encode(buf)

class subb_mi:
    """subb"""
    MNEMONIC = 'subb'
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
        digit = 0x5
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x80)
        reg = 0x5
        self.rm8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class subw_mi:
    """subw"""
    MNEMONIC = 'subw'
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
        digit = 0x5
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x5
        self.rm16.encode_rex_suffixes(buf, reg, 2, None)
        self.imm16.encode(buf)

class subl_mi:
    """subl"""
    MNEMONIC = 'subl'
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
        digit = 0x5
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x5
        self.rm32.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class subq_mi_sxl:
    """subq"""
    MNEMONIC = 'subq'
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
        digit = 0x5
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x5
        self.rm64.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class subl_mi_sxb:
    """subl"""
    MNEMONIC = 'subl'
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
        digit = 0x5
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x5
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class subq_mi_sxb:
    """subq"""
    MNEMONIC = 'subq'
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
        digit = 0x5
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x5
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class subb_mr:
    """subb"""
    MNEMONIC = 'subb'
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
        buf.put1(0x28)
        reg = self.r8.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class subw_mr:
    """subw"""
    MNEMONIC = 'subw'
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
        buf.put1(0x29)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class subl_mr:
    """subl"""
    MNEMONIC = 'subl'
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
        buf.put1(0x29)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class subq_mr:
    """subq"""
    MNEMONIC = 'subq'
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
        buf.put1(0x29)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class subb_rm:
    """subb"""
    MNEMONIC = 'subb'
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
        buf.put1(0x2a)
        reg = self.r8.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class subw_rm:
    """subw"""
    MNEMONIC = 'subw'
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
        buf.put1(0x2b)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class subl_rm:
    """subl"""
    MNEMONIC = 'subl'
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
        buf.put1(0x2b)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class subq_rm:
    """subq"""
    MNEMONIC = 'subq'
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
        buf.put1(0x2b)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class sbbb_i:
    """sbbb"""
    MNEMONIC = 'sbbb'
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
        buf.put1(0x1c)
        self.imm8.encode(buf)

class sbbw_i:
    """sbbw"""
    MNEMONIC = 'sbbw'
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
        buf.put1(0x1d)
        self.imm16.encode(buf)

class sbbl_i:
    """sbbl"""
    MNEMONIC = 'sbbl'
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
        buf.put1(0x1d)
        self.imm32.encode(buf)

class sbbq_i_sxl:
    """sbbq"""
    MNEMONIC = 'sbbq'
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
        buf.put1(0x1d)
        self.imm32.encode(buf)

class sbbb_mi:
    """sbbb"""
    MNEMONIC = 'sbbb'
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
        digit = 0x3
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x80)
        reg = 0x3
        self.rm8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class sbbw_mi:
    """sbbw"""
    MNEMONIC = 'sbbw'
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
        digit = 0x3
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x3
        self.rm16.encode_rex_suffixes(buf, reg, 2, None)
        self.imm16.encode(buf)

class sbbl_mi:
    """sbbl"""
    MNEMONIC = 'sbbl'
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
        digit = 0x3
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x3
        self.rm32.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class sbbq_mi_sxl:
    """sbbq"""
    MNEMONIC = 'sbbq'
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
        digit = 0x3
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x3
        self.rm64.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class sbbl_mi_sxb:
    """sbbl"""
    MNEMONIC = 'sbbl'
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
        digit = 0x3
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x3
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class sbbq_mi_sxb:
    """sbbq"""
    MNEMONIC = 'sbbq'
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
        digit = 0x3
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x83)
        reg = 0x3
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class sbbb_mr:
    """sbbb"""
    MNEMONIC = 'sbbb'
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
        buf.put1(0x18)
        reg = self.r8.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class sbbw_mr:
    """sbbw"""
    MNEMONIC = 'sbbw'
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
        buf.put1(0x19)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class sbbl_mr:
    """sbbl"""
    MNEMONIC = 'sbbl'
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
        buf.put1(0x19)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class sbbq_mr:
    """sbbq"""
    MNEMONIC = 'sbbq'
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
        buf.put1(0x19)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class sbbb_rm:
    """sbbb"""
    MNEMONIC = 'sbbb'
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
        buf.put1(0x1a)
        reg = self.r8.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class sbbw_rm:
    """sbbw"""
    MNEMONIC = 'sbbw'
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
        buf.put1(0x1b)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class sbbl_rm:
    """sbbl"""
    MNEMONIC = 'sbbl'
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
        buf.put1(0x1b)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class sbbq_rm:
    """sbbq"""
    MNEMONIC = 'sbbq'
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
        buf.put1(0x1b)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class subss_a:
    """subss"""
    MNEMONIC = 'subss'
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
        buf.put1(0x5c)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class subsd_a:
    """subsd"""
    MNEMONIC = 'subsd'
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
        buf.put1(0x5c)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class subps_a:
    """subps"""
    MNEMONIC = 'subps'
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
        buf.put1(0x5c)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class subpd_a:
    """subpd"""
    MNEMONIC = 'subpd'
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
        buf.put1(0x5c)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)
