"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class jmpq_m:
    """jmpq"""
    MNEMONIC = 'jmpq'
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
        w_bit = False
        digit = 0x4
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xff)
        reg = 0x4
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class jmp_d8:
    """jmp"""
    MNEMONIC = 'jmp'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0xeb)
        self.imm8.encode(buf)

class jmp_d32:
    """jmp"""
    MNEMONIC = 'jmp'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0xe9)
        self.imm32.encode(buf)

class ja_d8:
    """ja"""
    MNEMONIC = 'ja'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x77)
        self.imm8.encode(buf)

class ja_d32:
    """ja"""
    MNEMONIC = 'ja'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x87)
        self.imm32.encode(buf)

class jae_d8:
    """jae"""
    MNEMONIC = 'jae'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x73)
        self.imm8.encode(buf)

class jae_d32:
    """jae"""
    MNEMONIC = 'jae'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x83)
        self.imm32.encode(buf)

class jb_d8:
    """jb"""
    MNEMONIC = 'jb'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x72)
        self.imm8.encode(buf)

class jb_d32:
    """jb"""
    MNEMONIC = 'jb'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x82)
        self.imm32.encode(buf)

class jbe_d8:
    """jbe"""
    MNEMONIC = 'jbe'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x76)
        self.imm8.encode(buf)

class jbe_d32:
    """jbe"""
    MNEMONIC = 'jbe'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x86)
        self.imm32.encode(buf)

class je_d8:
    """je"""
    MNEMONIC = 'je'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x74)
        self.imm8.encode(buf)

class je_d32:
    """je"""
    MNEMONIC = 'je'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x84)
        self.imm32.encode(buf)

class jg_d8:
    """jg"""
    MNEMONIC = 'jg'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x7f)
        self.imm8.encode(buf)

class jg_d32:
    """jg"""
    MNEMONIC = 'jg'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x8f)
        self.imm32.encode(buf)

class jge_d8:
    """jge"""
    MNEMONIC = 'jge'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x7d)
        self.imm8.encode(buf)

class jge_d32:
    """jge"""
    MNEMONIC = 'jge'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x8d)
        self.imm32.encode(buf)

class jl_d8:
    """jl"""
    MNEMONIC = 'jl'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x7c)
        self.imm8.encode(buf)

class jl_d32:
    """jl"""
    MNEMONIC = 'jl'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x8c)
        self.imm32.encode(buf)

class jle_d8:
    """jle"""
    MNEMONIC = 'jle'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x7e)
        self.imm8.encode(buf)

class jle_d32:
    """jle"""
    MNEMONIC = 'jle'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x8e)
        self.imm32.encode(buf)

class jne_d8:
    """jne"""
    MNEMONIC = 'jne'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x75)
        self.imm8.encode(buf)

class jne_d32:
    """jne"""
    MNEMONIC = 'jne'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x85)
        self.imm32.encode(buf)

class jno_d8:
    """jno"""
    MNEMONIC = 'jno'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x71)
        self.imm8.encode(buf)

class jno_d32:
    """jno"""
    MNEMONIC = 'jno'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x81)
        self.imm32.encode(buf)

class jnp_d8:
    """jnp"""
    MNEMONIC = 'jnp'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x7b)
        self.imm8.encode(buf)

class jnp_d32:
    """jnp"""
    MNEMONIC = 'jnp'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x8b)
        self.imm32.encode(buf)

class jns_d8:
    """jns"""
    MNEMONIC = 'jns'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x79)
        self.imm8.encode(buf)

class jns_d32:
    """jns"""
    MNEMONIC = 'jns'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x89)
        self.imm32.encode(buf)

class jo_d8:
    """jo"""
    MNEMONIC = 'jo'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x70)
        self.imm8.encode(buf)

class jo_d32:
    """jo"""
    MNEMONIC = 'jo'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x80)
        self.imm32.encode(buf)

class jp_d8:
    """jp"""
    MNEMONIC = 'jp'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x7a)
        self.imm8.encode(buf)

class jp_d32:
    """jp"""
    MNEMONIC = 'jp'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x8a)
        self.imm32.encode(buf)

class js_d8:
    """js"""
    MNEMONIC = 'js'
    FIELDS = ('imm8',)

    def __init__(self, imm8):
        self.imm8 = imm8

    def encode(self, buf):
        buf.put1(0x78)
        self.imm8.encode(buf)

class js_d32:
    """js"""
    MNEMONIC = 'js'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0x0f)
        buf.put1(0x88)
        self.imm32.encode(buf)
