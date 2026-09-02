"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class negb_m:
    """negb"""
    MNEMONIC = 'negb'
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
        digit = 0x3
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf6)
        reg = 0x3
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class negw_m:
    """negw"""
    MNEMONIC = 'negw'
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
        digit = 0x3
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x3
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class negl_m:
    """negl"""
    MNEMONIC = 'negl'
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
        digit = 0x3
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x3
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class negq_m:
    """negq"""
    MNEMONIC = 'negq'
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
        digit = 0x3
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x3
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class notb_m:
    """notb"""
    MNEMONIC = 'notb'
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
        digit = 0x2
        rex = self.rm8.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf6)
        reg = 0x2
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class notw_m:
    """notw"""
    MNEMONIC = 'notw'
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
        digit = 0x2
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x2
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class notl_m:
    """notl"""
    MNEMONIC = 'notl'
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
        digit = 0x2
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x2
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class notq_m:
    """notq"""
    MNEMONIC = 'notq'
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
        digit = 0x2
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xf7)
        reg = 0x2
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class nop_zo:
    """nop"""
    MNEMONIC = 'nop'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        buf.put1(0x90)

class nopl_m:
    """nopl"""
    MNEMONIC = 'nopl'
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
        buf.put1(0x0f)
        buf.put1(0x1f)
        reg = 0x0
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class nop_1b:
    """nop"""
    MNEMONIC = 'nop'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        custom_encode.nop_1b(self, buf)

class nop_2b:
    """nop"""
    MNEMONIC = 'nop'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        custom_encode.nop_2b(self, buf)

class nop_3b:
    """nop"""
    MNEMONIC = 'nop'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        custom_encode.nop_3b(self, buf)

class nop_4b:
    """nop"""
    MNEMONIC = 'nop'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        custom_encode.nop_4b(self, buf)

class nop_5b:
    """nop"""
    MNEMONIC = 'nop'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        custom_encode.nop_5b(self, buf)

class nop_6b:
    """nop"""
    MNEMONIC = 'nop'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        custom_encode.nop_6b(self, buf)

class nop_7b:
    """nop"""
    MNEMONIC = 'nop'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        custom_encode.nop_7b(self, buf)

class nop_8b:
    """nop"""
    MNEMONIC = 'nop'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        custom_encode.nop_8b(self, buf)

class nop_9b:
    """nop"""
    MNEMONIC = 'nop'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        custom_encode.nop_9b(self, buf)
