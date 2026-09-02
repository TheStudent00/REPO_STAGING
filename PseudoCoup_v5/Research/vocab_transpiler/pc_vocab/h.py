"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class hlt_zo:
    """hlt"""
    MNEMONIC = 'hlt'
    FIELDS = ()

    def __init__(self):
        pass

    def encode(self, buf):
        buf.put1(0xf4)
