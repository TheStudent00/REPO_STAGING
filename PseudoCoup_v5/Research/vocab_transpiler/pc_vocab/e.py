"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class extractps_a:
    """extractps"""
    MNEMONIC = 'extractps'
    FIELDS = ('rm32', 'xmm1', 'imm8')

    def __init__(self, rm32, xmm1, imm8):
        self.rm32 = rm32
        self.xmm1 = xmm1
        self.imm8 = imm8

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
        buf.put1(0x3a)
        buf.put1(0x17)
        reg = self.xmm1.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)
