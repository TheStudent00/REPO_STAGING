"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class vpabsb_a:
    """vpabsb"""
    MNEMONIC = 'vpabsb'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x1c)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpabsw_a:
    """vpabsw"""
    MNEMONIC = 'vpabsw'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x1d)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpabsd_a:
    """vpabsd"""
    MNEMONIC = 'vpabsd'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x1e)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpabsd_c:
    """vpabsd"""
    MNEMONIC = 'vpabsd'
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
        ll = 0b00
        pp = 0b01
        mmm = 0b00010
        w = False
        bcast = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.two_op(reg, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x1e)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vpabsq_c:
    """vpabsq"""
    MNEMONIC = 'vpabsq'
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
        ll = 0b00
        pp = 0b01
        mmm = 0b00010
        w = True
        bcast = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.two_op(reg, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x1f)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vaddss_b:
    """vaddss"""
    MNEMONIC = 'vaddss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x58)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vaddsd_b:
    """vaddsd"""
    MNEMONIC = 'vaddsd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x58)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vaddps_b:
    """vaddps"""
    MNEMONIC = 'vaddps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x58)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vaddpd_b:
    """vaddpd"""
    MNEMONIC = 'vaddpd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x58)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpaddb_b:
    """vpaddb"""
    MNEMONIC = 'vpaddb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xfc)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpaddw_b:
    """vpaddw"""
    MNEMONIC = 'vpaddw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xfd)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpaddd_b:
    """vpaddd"""
    MNEMONIC = 'vpaddd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xfe)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpaddq_b:
    """vpaddq"""
    MNEMONIC = 'vpaddq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xd4)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpaddsb_b:
    """vpaddsb"""
    MNEMONIC = 'vpaddsb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xec)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpaddsw_b:
    """vpaddsw"""
    MNEMONIC = 'vpaddsw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xed)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpaddusb_b:
    """vpaddusb"""
    MNEMONIC = 'vpaddusb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xdc)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpaddusw_b:
    """vpaddusw"""
    MNEMONIC = 'vpaddusw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xdd)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vphaddw_b:
    """vphaddw"""
    MNEMONIC = 'vphaddw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x1)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vphaddd_b:
    """vphaddd"""
    MNEMONIC = 'vphaddd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vaddpd_c:
    """vaddpd"""
    MNEMONIC = 'vaddpd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        ll = 0b00
        pp = 0b01
        mmm = 0b00001
        w = True
        bcast = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x58)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vpalignr_b:
    """vpalignr"""
    MNEMONIC = 'vpalignr'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128', 'imm8')

    def __init__(self, xmm1, xmm2, xmm_m128, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vandps_b:
    """vandps"""
    MNEMONIC = 'vandps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x54)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vandpd_b:
    """vandpd"""
    MNEMONIC = 'vandpd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x54)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vandnps_b:
    """vandnps"""
    MNEMONIC = 'vandnps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x55)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vandnpd_b:
    """vandnpd"""
    MNEMONIC = 'vandnpd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x55)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpand_b:
    """vpand"""
    MNEMONIC = 'vpand'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xdb)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpandn_b:
    """vpandn"""
    MNEMONIC = 'vpandn'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xdf)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpavgb_b:
    """vpavgb"""
    MNEMONIC = 'vpavgb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xe0)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpavgw_b:
    """vpavgw"""
    MNEMONIC = 'vpavgw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xe3)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpopcntb_a:
    """vpopcntb"""
    MNEMONIC = 'vpopcntb'
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
        ll = 0b00
        pp = 0b01
        mmm = 0b00010
        w = False
        bcast = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.two_op(reg, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x54)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vpopcntw_a:
    """vpopcntw"""
    MNEMONIC = 'vpopcntw'
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
        ll = 0b00
        pp = 0b01
        mmm = 0b00010
        w = True
        bcast = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.two_op(reg, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x54)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vptest_rm:
    """vptest"""
    MNEMONIC = 'vptest'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x17)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vucomiss_a:
    """vucomiss"""
    MNEMONIC = 'vucomiss'
    FIELDS = ('xmm2', 'xmm_m32')

    def __init__(self, xmm2, xmm_m32):
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2e)
        reg = self.xmm2.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vucomisd_a:
    """vucomisd"""
    MNEMONIC = 'vucomisd'
    FIELDS = ('xmm2', 'xmm_m64')

    def __init__(self, xmm2, xmm_m64):
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2e)
        reg = self.xmm2.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vcmpss_b:
    """vcmpss"""
    MNEMONIC = 'vcmpss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32', 'imm8')

    def __init__(self, xmm1, xmm2, xmm_m32, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xc2)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vcmpsd_b:
    """vcmpsd"""
    MNEMONIC = 'vcmpsd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64', 'imm8')

    def __init__(self, xmm1, xmm2, xmm_m64, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xc2)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vcmpps_b:
    """vcmpps"""
    MNEMONIC = 'vcmpps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128', 'imm8')

    def __init__(self, xmm1, xmm2, xmm_m128, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xc2)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vcmppd_b:
    """vcmppd"""
    MNEMONIC = 'vcmppd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128', 'imm8')

    def __init__(self, xmm1, xmm2, xmm_m128, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xc2)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vpcmpeqb_b:
    """vpcmpeqb"""
    MNEMONIC = 'vpcmpeqb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x74)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpcmpeqw_b:
    """vpcmpeqw"""
    MNEMONIC = 'vpcmpeqw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x75)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpcmpeqd_b:
    """vpcmpeqd"""
    MNEMONIC = 'vpcmpeqd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x76)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpcmpeqq_b:
    """vpcmpeqq"""
    MNEMONIC = 'vpcmpeqq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x29)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpcmpgtb_b:
    """vpcmpgtb"""
    MNEMONIC = 'vpcmpgtb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x64)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpcmpgtw_b:
    """vpcmpgtw"""
    MNEMONIC = 'vpcmpgtw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x65)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpcmpgtd_b:
    """vpcmpgtd"""
    MNEMONIC = 'vpcmpgtd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x66)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpcmpgtq_b:
    """vpcmpgtq"""
    MNEMONIC = 'vpcmpgtq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x37)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vcvtps2pd_a:
    """vcvtps2pd"""
    MNEMONIC = 'vcvtps2pd'
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
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5a)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vcvttps2dq_a:
    """vcvttps2dq"""
    MNEMONIC = 'vcvttps2dq'
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
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5b)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vcvtss2sd_b:
    """vcvtss2sd"""
    MNEMONIC = 'vcvtss2sd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5a)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vcvtss2si_a:
    """vcvtss2si"""
    MNEMONIC = 'vcvtss2si'
    FIELDS = ('r32', 'xmm_m32')

    def __init__(self, r32, xmm_m32):
        self.r32 = r32
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.r32.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2d)
        reg = self.r32.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vcvtss2si_aq:
    """vcvtss2si"""
    MNEMONIC = 'vcvtss2si'
    FIELDS = ('r64', 'xmm_m32')

    def __init__(self, r64, xmm_m32):
        self.r64 = r64
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = True
        reg = self.r64.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2d)
        reg = self.r64.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vcvttss2si_a:
    """vcvttss2si"""
    MNEMONIC = 'vcvttss2si'
    FIELDS = ('r32', 'xmm_m32')

    def __init__(self, r32, xmm_m32):
        self.r32 = r32
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.r32.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2c)
        reg = self.r32.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vcvttss2si_aq:
    """vcvttss2si"""
    MNEMONIC = 'vcvttss2si'
    FIELDS = ('r64', 'xmm_m32')

    def __init__(self, r64, xmm_m32):
        self.r64 = r64
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = True
        reg = self.r64.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2c)
        reg = self.r64.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vcvtpd2ps_a:
    """vcvtpd2ps_a"""
    MNEMONIC = 'vcvtpd2ps_a'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5a)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vcvttpd2dq_a:
    """vcvttpd2dq_a"""
    MNEMONIC = 'vcvttpd2dq_a'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xe6)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vcvtsd2ss_b:
    """vcvtsd2ss"""
    MNEMONIC = 'vcvtsd2ss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5a)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vcvtsd2si_a:
    """vcvtsd2si"""
    MNEMONIC = 'vcvtsd2si'
    FIELDS = ('r32', 'xmm_m64')

    def __init__(self, r32, xmm_m64):
        self.r32 = r32
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.r32.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2d)
        reg = self.r32.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vcvtsd2si_aq:
    """vcvtsd2si"""
    MNEMONIC = 'vcvtsd2si'
    FIELDS = ('r64', 'xmm_m64')

    def __init__(self, r64, xmm_m64):
        self.r64 = r64
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = True
        reg = self.r64.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2d)
        reg = self.r64.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vcvttsd2si_a:
    """vcvttsd2si"""
    MNEMONIC = 'vcvttsd2si'
    FIELDS = ('r32', 'xmm_m64')

    def __init__(self, r32, xmm_m64):
        self.r32 = r32
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.r32.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2c)
        reg = self.r32.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vcvttsd2si_aq:
    """vcvttsd2si"""
    MNEMONIC = 'vcvttsd2si'
    FIELDS = ('r64', 'xmm_m64')

    def __init__(self, r64, xmm_m64):
        self.r64 = r64
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = True
        reg = self.r64.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2c)
        reg = self.r64.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vcvtdq2pd_a:
    """vcvtdq2pd"""
    MNEMONIC = 'vcvtdq2pd'
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
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xe6)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vcvtdq2ps_a:
    """vcvtdq2ps"""
    MNEMONIC = 'vcvtdq2ps'
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
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5b)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vcvtsi2sdl_b:
    """vcvtsi2sdl"""
    MNEMONIC = 'vcvtsi2sdl'
    FIELDS = ('xmm1', 'xmm2', 'rm32')

    def __init__(self, xmm1, xmm2, rm32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.rm32 = rm32

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2a)
        reg = self.xmm1.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class vcvtsi2sdq_b:
    """vcvtsi2sdq"""
    MNEMONIC = 'vcvtsi2sdq'
    FIELDS = ('xmm1', 'xmm2', 'rm64')

    def __init__(self, xmm1, xmm2, rm64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.rm64 = rm64

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.rm64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2a)
        reg = self.xmm1.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class vcvtsi2ssl_b:
    """vcvtsi2ssl"""
    MNEMONIC = 'vcvtsi2ssl'
    FIELDS = ('xmm1', 'xmm2', 'rm32')

    def __init__(self, xmm1, xmm2, rm32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.rm32 = rm32

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2a)
        reg = self.xmm1.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class vcvtsi2ssq_b:
    """vcvtsi2ssq"""
    MNEMONIC = 'vcvtsi2ssq'
    FIELDS = ('xmm1', 'xmm2', 'rm64')

    def __init__(self, xmm1, xmm2, rm64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.rm64 = rm64

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.rm64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2a)
        reg = self.xmm1.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class vcvtudq2ps_a:
    """vcvtudq2ps"""
    MNEMONIC = 'vcvtudq2ps'
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
        ll = 0b00
        pp = 0b11
        mmm = 0b00001
        w = False
        bcast = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.two_op(reg, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x7a)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vdivss_b:
    """vdivss"""
    MNEMONIC = 'vdivss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5e)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vdivsd_b:
    """vdivsd"""
    MNEMONIC = 'vdivsd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5e)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vdivps_b:
    """vdivps"""
    MNEMONIC = 'vdivps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5e)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vdivpd_b:
    """vdivpd"""
    MNEMONIC = 'vdivpd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5e)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfmadd132ss_a:
    """vfmadd132ss"""
    MNEMONIC = 'vfmadd132ss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x99)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vfmadd213ss_a:
    """vfmadd213ss"""
    MNEMONIC = 'vfmadd213ss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xa9)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vfmadd231ss_a:
    """vfmadd231ss"""
    MNEMONIC = 'vfmadd231ss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xb9)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vfmadd132sd_a:
    """vfmadd132sd"""
    MNEMONIC = 'vfmadd132sd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x99)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vfmadd213sd_a:
    """vfmadd213sd"""
    MNEMONIC = 'vfmadd213sd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xa9)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vfmadd231sd_a:
    """vfmadd231sd"""
    MNEMONIC = 'vfmadd231sd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xb9)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vfmadd132ps_a:
    """vfmadd132ps"""
    MNEMONIC = 'vfmadd132ps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x98)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfmadd213ps_a:
    """vfmadd213ps"""
    MNEMONIC = 'vfmadd213ps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xa8)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfmadd231ps_a:
    """vfmadd231ps"""
    MNEMONIC = 'vfmadd231ps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xb8)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfmadd132pd_a:
    """vfmadd132pd"""
    MNEMONIC = 'vfmadd132pd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x98)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfmadd213pd_a:
    """vfmadd213pd"""
    MNEMONIC = 'vfmadd213pd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xa8)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfmadd231pd_a:
    """vfmadd231pd"""
    MNEMONIC = 'vfmadd231pd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xb8)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfnmadd132ss_a:
    """vfnmadd132ss"""
    MNEMONIC = 'vfnmadd132ss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x9d)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vfnmadd213ss_a:
    """vfnmadd213ss"""
    MNEMONIC = 'vfnmadd213ss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xad)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vfnmadd231ss_a:
    """vfnmadd231ss"""
    MNEMONIC = 'vfnmadd231ss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xbd)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vfnmadd132sd_a:
    """vfnmadd132sd"""
    MNEMONIC = 'vfnmadd132sd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x9d)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vfnmadd213sd_a:
    """vfnmadd213sd"""
    MNEMONIC = 'vfnmadd213sd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xad)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vfnmadd231sd_a:
    """vfnmadd231sd"""
    MNEMONIC = 'vfnmadd231sd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xbd)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vfnmadd132ps_a:
    """vfnmadd132ps"""
    MNEMONIC = 'vfnmadd132ps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x9c)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfnmadd213ps_a:
    """vfnmadd213ps"""
    MNEMONIC = 'vfnmadd213ps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xac)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfnmadd231ps_a:
    """vfnmadd231ps"""
    MNEMONIC = 'vfnmadd231ps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xbc)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfnmadd132pd_a:
    """vfnmadd132pd"""
    MNEMONIC = 'vfnmadd132pd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x9c)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfnmadd213pd_a:
    """vfnmadd213pd"""
    MNEMONIC = 'vfnmadd213pd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xac)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfnmadd231pd_a:
    """vfnmadd231pd"""
    MNEMONIC = 'vfnmadd231pd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xbc)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfmsub132ss_a:
    """vfmsub132ss"""
    MNEMONIC = 'vfmsub132ss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x9b)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vfmsub213ss_a:
    """vfmsub213ss"""
    MNEMONIC = 'vfmsub213ss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xab)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vfmsub231ss_a:
    """vfmsub231ss"""
    MNEMONIC = 'vfmsub231ss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xbb)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vfmsub132sd_a:
    """vfmsub132sd"""
    MNEMONIC = 'vfmsub132sd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x9b)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vfmsub213sd_a:
    """vfmsub213sd"""
    MNEMONIC = 'vfmsub213sd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xab)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vfmsub231sd_a:
    """vfmsub231sd"""
    MNEMONIC = 'vfmsub231sd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xbb)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vfmsub132ps_a:
    """vfmsub132ps"""
    MNEMONIC = 'vfmsub132ps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x9a)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfmsub213ps_a:
    """vfmsub213ps"""
    MNEMONIC = 'vfmsub213ps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xaa)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfmsub231ps_a:
    """vfmsub231ps"""
    MNEMONIC = 'vfmsub231ps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xba)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfmsub132pd_a:
    """vfmsub132pd"""
    MNEMONIC = 'vfmsub132pd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x9a)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfmsub213pd_a:
    """vfmsub213pd"""
    MNEMONIC = 'vfmsub213pd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xaa)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfmsub231pd_a:
    """vfmsub231pd"""
    MNEMONIC = 'vfmsub231pd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xba)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfnmsub132ss_a:
    """vfnmsub132ss"""
    MNEMONIC = 'vfnmsub132ss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x9f)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vfnmsub213ss_a:
    """vfnmsub213ss"""
    MNEMONIC = 'vfnmsub213ss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xaf)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vfnmsub231ss_a:
    """vfnmsub231ss"""
    MNEMONIC = 'vfnmsub231ss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xbf)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vfnmsub132sd_a:
    """vfnmsub132sd"""
    MNEMONIC = 'vfnmsub132sd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x9f)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vfnmsub213sd_a:
    """vfnmsub213sd"""
    MNEMONIC = 'vfnmsub213sd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xaf)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vfnmsub231sd_a:
    """vfnmsub231sd"""
    MNEMONIC = 'vfnmsub231sd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xbf)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vfnmsub132ps_a:
    """vfnmsub132ps"""
    MNEMONIC = 'vfnmsub132ps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x9e)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfnmsub213ps_a:
    """vfnmsub213ps"""
    MNEMONIC = 'vfnmsub213ps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xae)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfnmsub231ps_a:
    """vfnmsub231ps"""
    MNEMONIC = 'vfnmsub231ps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xbe)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfnmsub132pd_a:
    """vfnmsub132pd"""
    MNEMONIC = 'vfnmsub132pd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x9e)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfnmsub213pd_a:
    """vfnmsub213pd"""
    MNEMONIC = 'vfnmsub213pd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xae)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vfnmsub231pd_a:
    """vfnmsub231pd"""
    MNEMONIC = 'vfnmsub231pd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xbe)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vextractps_b:
    """vextractps"""
    MNEMONIC = 'vextractps'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm1.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x17)
        reg = self.xmm1.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vpextrb_a:
    """vpextrb"""
    MNEMONIC = 'vpextrb'
    FIELDS = ('rm32', 'xmm2', 'imm8')

    def __init__(self, rm32, xmm2, imm8):
        self.rm32 = rm32
        self.xmm2 = xmm2
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm2.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x14)
        reg = self.xmm2.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vpextrw_a:
    """vpextrw"""
    MNEMONIC = 'vpextrw'
    FIELDS = ('r32', 'xmm2', 'imm8')

    def __init__(self, r32, xmm2, imm8):
        self.r32 = r32
        self.xmm2 = xmm2
        self.imm8 = imm8

    def encode(self, buf):
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.r32.enc()
        rm = self.xmm2.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xc5)
        reg = self.r32.enc()
        self.xmm2.encode_modrm(buf, reg)
        self.imm8.encode(buf)

class vpextrw_b:
    """vpextrw"""
    MNEMONIC = 'vpextrw'
    FIELDS = ('rm32', 'xmm2', 'imm8')

    def __init__(self, rm32, xmm2, imm8):
        self.rm32 = rm32
        self.xmm2 = xmm2
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm2.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x15)
        reg = self.xmm2.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vpextrd_a:
    """vpextrd"""
    MNEMONIC = 'vpextrd'
    FIELDS = ('rm32', 'xmm2', 'imm8')

    def __init__(self, rm32, xmm2, imm8):
        self.rm32 = rm32
        self.xmm2 = xmm2
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm2.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x16)
        reg = self.xmm2.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vpextrq_a:
    """vpextrq"""
    MNEMONIC = 'vpextrq'
    FIELDS = ('rm64', 'xmm2', 'imm8')

    def __init__(self, rm64, xmm2, imm8):
        self.rm64 = rm64
        self.xmm2 = xmm2
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = True
        reg = self.xmm2.enc()
        rm = self.rm64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x16)
        reg = self.xmm2.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vinsertps_b:
    """vinsertps"""
    MNEMONIC = 'vinsertps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32', 'imm8')

    def __init__(self, xmm1, xmm2, xmm_m32, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x21)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vpinsrb_b:
    """vpinsrb"""
    MNEMONIC = 'vpinsrb'
    FIELDS = ('xmm1', 'xmm2', 'rm32', 'imm8')

    def __init__(self, xmm1, xmm2, rm32, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.rm32 = rm32
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x20)
        reg = self.xmm1.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vpinsrw_b:
    """vpinsrw"""
    MNEMONIC = 'vpinsrw'
    FIELDS = ('xmm1', 'xmm2', 'rm32', 'imm8')

    def __init__(self, xmm1, xmm2, rm32, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.rm32 = rm32
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xc4)
        reg = self.xmm1.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vpinsrd_b:
    """vpinsrd"""
    MNEMONIC = 'vpinsrd'
    FIELDS = ('xmm1', 'xmm2', 'rm32', 'imm8')

    def __init__(self, xmm1, xmm2, rm32, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.rm32 = rm32
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x22)
        reg = self.xmm1.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vpinsrq_b:
    """vpinsrq"""
    MNEMONIC = 'vpinsrq'
    FIELDS = ('xmm1', 'xmm2', 'rm64', 'imm8')

    def __init__(self, xmm1, xmm2, rm64, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.rm64 = rm64
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = True
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.rm64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x22)
        reg = self.xmm1.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vmovmskps_rm:
    """vmovmskps"""
    MNEMONIC = 'vmovmskps'
    FIELDS = ('r32', 'xmm2')

    def __init__(self, r32, xmm2):
        self.r32 = r32
        self.xmm2 = xmm2

    def encode(self, buf):
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.r32.enc()
        rm = self.xmm2.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x50)
        reg = self.r32.enc()
        self.xmm2.encode_modrm(buf, reg)

class vmovmskpd_rm:
    """vmovmskpd"""
    MNEMONIC = 'vmovmskpd'
    FIELDS = ('r32', 'xmm2')

    def __init__(self, r32, xmm2):
        self.r32 = r32
        self.xmm2 = xmm2

    def encode(self, buf):
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.r32.enc()
        rm = self.xmm2.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x50)
        reg = self.r32.enc()
        self.xmm2.encode_modrm(buf, reg)

class vpmovmskb_rm:
    """vpmovmskb"""
    MNEMONIC = 'vpmovmskb'
    FIELDS = ('r32', 'xmm2')

    def __init__(self, r32, xmm2):
        self.r32 = r32
        self.xmm2 = xmm2

    def encode(self, buf):
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.r32.enc()
        rm = self.xmm2.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xd7)
        reg = self.r32.enc()
        self.xmm2.encode_modrm(buf, reg)

class vmovhps_b:
    """vmovhps"""
    MNEMONIC = 'vmovhps'
    FIELDS = ('xmm2', 'xmm1', 'm64')

    def __init__(self, xmm2, xmm1, m64):
        self.xmm2 = xmm2
        self.xmm1 = xmm1
        self.m64 = m64

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm2.enc()
        vvvv = self.xmm1.enc()
        rm = self.m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x16)
        reg = self.xmm2.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class vmovlhps_rvm:
    """vmovlhps"""
    MNEMONIC = 'vmovlhps'
    FIELDS = ('xmm1', 'xmm2', 'xmm3')

    def __init__(self, xmm1, xmm2, xmm3):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm3 = xmm3

    def encode(self, buf):
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm3.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x16)
        reg = self.xmm1.enc()
        self.xmm3.encode_modrm(buf, reg)

class vmovddup_a:
    """vmovddup"""
    MNEMONIC = 'vmovddup'
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
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x12)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vpblendw_rvmi:
    """vpblendw"""
    MNEMONIC = 'vpblendw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128', 'imm8')

    def __init__(self, xmm1, xmm2, xmm_m128, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xe)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vpblendvb_rvmr:
    """vpblendvb"""
    MNEMONIC = 'vpblendvb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128', 'xmm3')

    def __init__(self, xmm1, xmm2, xmm_m128, xmm3):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128
        self.xmm3 = xmm3

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x4c)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        buf.put1(self.xmm3.enc() << 4)

class vblendvps_rvmr:
    """vblendvps"""
    MNEMONIC = 'vblendvps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128', 'xmm3')

    def __init__(self, xmm1, xmm2, xmm_m128, xmm3):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128
        self.xmm3 = xmm3

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x4a)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        buf.put1(self.xmm3.enc() << 4)

class vblendvpd_rvmr:
    """vblendvpd"""
    MNEMONIC = 'vblendvpd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128', 'xmm3')

    def __init__(self, xmm1, xmm2, xmm_m128, xmm3):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128
        self.xmm3 = xmm3

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x4b)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        buf.put1(self.xmm3.enc() << 4)

class vshufpd_b:
    """vshufpd"""
    MNEMONIC = 'vshufpd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128', 'imm8')

    def __init__(self, xmm1, xmm2, xmm_m128, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xc6)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vshufps_b:
    """vshufps"""
    MNEMONIC = 'vshufps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128', 'imm8')

    def __init__(self, xmm1, xmm2, xmm_m128, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xc6)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vpshufb_b:
    """vpshufb"""
    MNEMONIC = 'vpshufb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x0)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpshufd_a:
    """vpshufd"""
    MNEMONIC = 'vpshufd'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x70)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vpshuflw_a:
    """vpshuflw"""
    MNEMONIC = 'vpshuflw'
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
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x70)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vpshufhw_a:
    """vpshufhw"""
    MNEMONIC = 'vpshufhw'
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
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x70)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vbroadcastss_a_m:
    """vbroadcastss"""
    MNEMONIC = 'vbroadcastss'
    FIELDS = ('xmm1', 'm32')

    def __init__(self, xmm1, m32):
        self.xmm1 = xmm1
        self.m32 = m32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.m32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x18)
        reg = self.xmm1.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class vbroadcastss_a_r:
    """vbroadcastss"""
    MNEMONIC = 'vbroadcastss'
    FIELDS = ('xmm1', 'xmm2')

    def __init__(self, xmm1, xmm2):
        self.xmm1 = xmm1
        self.xmm2 = xmm2

    def encode(self, buf):
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm2.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x18)
        reg = self.xmm1.enc()
        self.xmm2.encode_modrm(buf, reg)

class vpbroadcastb_a:
    """vpbroadcastb"""
    MNEMONIC = 'vpbroadcastb'
    FIELDS = ('xmm1', 'xmm_m8')

    def __init__(self, xmm1, xmm_m8):
        self.xmm1 = xmm1
        self.xmm_m8 = xmm_m8

    def encode(self, buf):
        if isinstance(self.xmm_m8, Mem):
            xmm_m8 = self.xmm_m8
            trap_code = xmm_m8.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m8.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x78)
        reg = self.xmm1.enc()
        self.xmm_m8.encode_rex_suffixes(buf, reg, 0, None)

class vpbroadcastw_a:
    """vpbroadcastw"""
    MNEMONIC = 'vpbroadcastw'
    FIELDS = ('xmm1', 'xmm_m16')

    def __init__(self, xmm1, xmm_m16):
        self.xmm1 = xmm1
        self.xmm_m16 = xmm_m16

    def encode(self, buf):
        if isinstance(self.xmm_m16, Mem):
            xmm_m16 = self.xmm_m16
            trap_code = xmm_m16.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m16.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x79)
        reg = self.xmm1.enc()
        self.xmm_m16.encode_rex_suffixes(buf, reg, 0, None)

class vpbroadcastd_a:
    """vpbroadcastd"""
    MNEMONIC = 'vpbroadcastd'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x58)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vpbroadcastq_a:
    """vpbroadcastq"""
    MNEMONIC = 'vpbroadcastq'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x59)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vpermi2b_a:
    """vpermi2b"""
    MNEMONIC = 'vpermi2b'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        ll = 0b00
        pp = 0b01
        mmm = 0b00010
        w = False
        bcast = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x75)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vmaxss_b:
    """vmaxss"""
    MNEMONIC = 'vmaxss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5f)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vmaxsd_b:
    """vmaxsd"""
    MNEMONIC = 'vmaxsd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5f)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vmaxps_b:
    """vmaxps"""
    MNEMONIC = 'vmaxps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5f)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vmaxpd_b:
    """vmaxpd"""
    MNEMONIC = 'vmaxpd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5f)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmaxsb_b:
    """vpmaxsb"""
    MNEMONIC = 'vpmaxsb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x3c)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmaxsw_b:
    """vpmaxsw"""
    MNEMONIC = 'vpmaxsw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xee)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmaxsd_b:
    """vpmaxsd"""
    MNEMONIC = 'vpmaxsd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x3d)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmaxub_b:
    """vpmaxub"""
    MNEMONIC = 'vpmaxub'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xde)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmaxuw_b:
    """vpmaxuw"""
    MNEMONIC = 'vpmaxuw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x3e)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmaxud_b:
    """vpmaxud"""
    MNEMONIC = 'vpmaxud'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x3f)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vminss_b:
    """vminss"""
    MNEMONIC = 'vminss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5d)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vminsd_b:
    """vminsd"""
    MNEMONIC = 'vminsd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5d)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vminps_b:
    """vminps"""
    MNEMONIC = 'vminps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5d)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vminpd_b:
    """vminpd"""
    MNEMONIC = 'vminpd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5d)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpminsb_b:
    """vpminsb"""
    MNEMONIC = 'vpminsb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x38)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpminsw_b:
    """vpminsw"""
    MNEMONIC = 'vpminsw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xea)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpminsd_b:
    """vpminsd"""
    MNEMONIC = 'vpminsd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x39)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpminub_b:
    """vpminub"""
    MNEMONIC = 'vpminub'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xda)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpminuw_b:
    """vpminuw"""
    MNEMONIC = 'vpminuw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x3a)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpminud_b:
    """vpminud"""
    MNEMONIC = 'vpminud'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x3b)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vmovd_a:
    """vmovd"""
    MNEMONIC = 'vmovd'
    FIELDS = ('xmm1', 'rm32')

    def __init__(self, xmm1, rm32):
        self.xmm1 = xmm1
        self.rm32 = rm32

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x6e)
        reg = self.xmm1.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class vmovq_a:
    """vmovq"""
    MNEMONIC = 'vmovq'
    FIELDS = ('xmm1', 'rm64')

    def __init__(self, xmm1, rm64):
        self.xmm1 = xmm1
        self.rm64 = rm64

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = True
        reg = self.xmm1.enc()
        rm = self.rm64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x6e)
        reg = self.xmm1.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class vmovd_b:
    """vmovd"""
    MNEMONIC = 'vmovd'
    FIELDS = ('rm32', 'xmm2')

    def __init__(self, rm32, xmm2):
        self.rm32 = rm32
        self.xmm2 = xmm2

    def encode(self, buf):
        if isinstance(self.rm32, Mem):
            rm32 = self.rm32
            trap_code = rm32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm2.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x7e)
        reg = self.xmm2.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class vmovq_b:
    """vmovq"""
    MNEMONIC = 'vmovq'
    FIELDS = ('rm64', 'xmm2')

    def __init__(self, rm64, xmm2):
        self.rm64 = rm64
        self.xmm2 = xmm2

    def encode(self, buf):
        if isinstance(self.rm64, Mem):
            rm64 = self.rm64
            trap_code = rm64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = True
        reg = self.xmm2.enc()
        rm = self.rm64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x7e)
        reg = self.xmm2.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class vmovss_d:
    """vmovss"""
    MNEMONIC = 'vmovss'
    FIELDS = ('xmm1', 'm32')

    def __init__(self, xmm1, m32):
        self.xmm1 = xmm1
        self.m32 = m32

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.m32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x10)
        reg = self.xmm1.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class vmovss_b:
    """vmovss"""
    MNEMONIC = 'vmovss'
    FIELDS = ('xmm1', 'xmm2', 'xmm3')

    def __init__(self, xmm1, xmm2, xmm3):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm3 = xmm3

    def encode(self, buf):
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm3.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x10)
        reg = self.xmm1.enc()
        self.xmm3.encode_modrm(buf, reg)

class vmovss_c_m:
    """vmovss"""
    MNEMONIC = 'vmovss'
    FIELDS = ('m32', 'xmm1')

    def __init__(self, m32, xmm1):
        self.m32 = m32
        self.xmm1 = xmm1

    def encode(self, buf):
        trap_code = self.m32.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.m32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x11)
        reg = self.xmm1.enc()
        self.m32.encode_rex_suffixes(buf, reg, 0, None)

class vmovsd_d:
    """vmovsd"""
    MNEMONIC = 'vmovsd'
    FIELDS = ('xmm1', 'm64')

    def __init__(self, xmm1, m64):
        self.xmm1 = xmm1
        self.m64 = m64

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x10)
        reg = self.xmm1.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class vmovsd_b:
    """vmovsd"""
    MNEMONIC = 'vmovsd'
    FIELDS = ('xmm1', 'xmm2', 'xmm3')

    def __init__(self, xmm1, xmm2, xmm3):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm3 = xmm3

    def encode(self, buf):
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm3.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x10)
        reg = self.xmm1.enc()
        self.xmm3.encode_modrm(buf, reg)

class vmovsd_c_m:
    """vmovsd"""
    MNEMONIC = 'vmovsd'
    FIELDS = ('m64', 'xmm1')

    def __init__(self, m64, xmm1):
        self.m64 = m64
        self.xmm1 = xmm1

    def encode(self, buf):
        trap_code = self.m64.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x11)
        reg = self.xmm1.enc()
        self.m64.encode_rex_suffixes(buf, reg, 0, None)

class vmovapd_a:
    """vmovapd"""
    MNEMONIC = 'vmovapd'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x28)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vmovapd_b:
    """vmovapd"""
    MNEMONIC = 'vmovapd'
    FIELDS = ('xmm_m128', 'xmm1')

    def __init__(self, xmm_m128, xmm1):
        self.xmm_m128 = xmm_m128
        self.xmm1 = xmm1

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x29)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vmovaps_a:
    """vmovaps"""
    MNEMONIC = 'vmovaps'
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
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x28)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vmovaps_b:
    """vmovaps"""
    MNEMONIC = 'vmovaps'
    FIELDS = ('xmm_m128', 'xmm1')

    def __init__(self, xmm_m128, xmm1):
        self.xmm_m128 = xmm_m128
        self.xmm1 = xmm1

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x29)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vmovdqa_a:
    """vmovdqa"""
    MNEMONIC = 'vmovdqa'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x6f)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vmovdqa_b:
    """vmovdqa"""
    MNEMONIC = 'vmovdqa'
    FIELDS = ('xmm_m128', 'xmm1')

    def __init__(self, xmm_m128, xmm1):
        self.xmm_m128 = xmm_m128
        self.xmm1 = xmm1

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x7f)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vmovupd_a:
    """vmovupd"""
    MNEMONIC = 'vmovupd'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x10)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vmovupd_b:
    """vmovupd"""
    MNEMONIC = 'vmovupd'
    FIELDS = ('xmm_m128', 'xmm1')

    def __init__(self, xmm_m128, xmm1):
        self.xmm_m128 = xmm_m128
        self.xmm1 = xmm1

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x11)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vmovups_a:
    """vmovups"""
    MNEMONIC = 'vmovups'
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
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x10)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vmovups_b:
    """vmovups"""
    MNEMONIC = 'vmovups'
    FIELDS = ('xmm_m128', 'xmm1')

    def __init__(self, xmm_m128, xmm1):
        self.xmm_m128 = xmm_m128
        self.xmm1 = xmm1

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x11)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vmovdqu_a:
    """vmovdqu"""
    MNEMONIC = 'vmovdqu'
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
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x6f)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vmovdqu_b:
    """vmovdqu"""
    MNEMONIC = 'vmovdqu'
    FIELDS = ('xmm_m128', 'xmm1')

    def __init__(self, xmm_m128, xmm1):
        self.xmm_m128 = xmm_m128
        self.xmm1 = xmm1

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x7f)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmovsxbw_a:
    """vpmovsxbw"""
    MNEMONIC = 'vpmovsxbw'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x20)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vpmovsxbd_a:
    """vpmovsxbd"""
    MNEMONIC = 'vpmovsxbd'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x21)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vpmovsxbq_a:
    """vpmovsxbq"""
    MNEMONIC = 'vpmovsxbq'
    FIELDS = ('xmm1', 'xmm_m16')

    def __init__(self, xmm1, xmm_m16):
        self.xmm1 = xmm1
        self.xmm_m16 = xmm_m16

    def encode(self, buf):
        if isinstance(self.xmm_m16, Mem):
            xmm_m16 = self.xmm_m16
            trap_code = xmm_m16.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m16.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x22)
        reg = self.xmm1.enc()
        self.xmm_m16.encode_rex_suffixes(buf, reg, 0, None)

class vpmovsxwd_a:
    """vpmovsxwd"""
    MNEMONIC = 'vpmovsxwd'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x23)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vpmovsxwq_a:
    """vpmovsxwq"""
    MNEMONIC = 'vpmovsxwq'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x24)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vpmovsxdq_a:
    """vpmovsxdq"""
    MNEMONIC = 'vpmovsxdq'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x25)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vpmovzxbw_a:
    """vpmovzxbw"""
    MNEMONIC = 'vpmovzxbw'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x30)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vpmovzxbd_a:
    """vpmovzxbd"""
    MNEMONIC = 'vpmovzxbd'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x31)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vpmovzxbq_a:
    """vpmovzxbq"""
    MNEMONIC = 'vpmovzxbq'
    FIELDS = ('xmm1', 'xmm_m16')

    def __init__(self, xmm1, xmm_m16):
        self.xmm1 = xmm1
        self.xmm_m16 = xmm_m16

    def encode(self, buf):
        if isinstance(self.xmm_m16, Mem):
            xmm_m16 = self.xmm_m16
            trap_code = xmm_m16.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m16.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x32)
        reg = self.xmm1.enc()
        self.xmm_m16.encode_rex_suffixes(buf, reg, 0, None)

class vpmovzxwd_a:
    """vpmovzxwd"""
    MNEMONIC = 'vpmovzxwd'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x33)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vpmovzxwq_a:
    """vpmovzxwq"""
    MNEMONIC = 'vpmovzxwq'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x34)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vpmovzxdq_a:
    """vpmovzxdq"""
    MNEMONIC = 'vpmovzxdq'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x35)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vmulss_b:
    """vmulss"""
    MNEMONIC = 'vmulss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x59)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vmulsd_b:
    """vmulsd"""
    MNEMONIC = 'vmulsd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x59)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vmulps_b:
    """vmulps"""
    MNEMONIC = 'vmulps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x59)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vmulpd_b:
    """vmulpd"""
    MNEMONIC = 'vmulpd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x59)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmuldq_b:
    """vpmuldq"""
    MNEMONIC = 'vpmuldq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x28)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmulhrsw_b:
    """vpmulhrsw"""
    MNEMONIC = 'vpmulhrsw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xb)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmulhuw_b:
    """vpmulhuw"""
    MNEMONIC = 'vpmulhuw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xe4)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmulhw_b:
    """vpmulhw"""
    MNEMONIC = 'vpmulhw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xe5)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmulld_b:
    """vpmulld"""
    MNEMONIC = 'vpmulld'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x40)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmullw_b:
    """vpmullw"""
    MNEMONIC = 'vpmullw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xd5)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmuludq_b:
    """vpmuludq"""
    MNEMONIC = 'vpmuludq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf4)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmulld_c:
    """vpmulld"""
    MNEMONIC = 'vpmulld'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        ll = 0b00
        pp = 0b01
        mmm = 0b00010
        w = False
        bcast = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x40)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vpmullq_c:
    """vpmullq"""
    MNEMONIC = 'vpmullq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        ll = 0b00
        pp = 0b01
        mmm = 0b00010
        w = True
        bcast = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x40)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vorps_b:
    """vorps"""
    MNEMONIC = 'vorps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x56)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vorpd_b:
    """vorpd"""
    MNEMONIC = 'vorpd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x56)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpor_b:
    """vpor"""
    MNEMONIC = 'vpor'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xeb)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpacksswb_b:
    """vpacksswb"""
    MNEMONIC = 'vpacksswb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x63)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpackssdw_b:
    """vpackssdw"""
    MNEMONIC = 'vpackssdw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x6b)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpackuswb_b:
    """vpackuswb"""
    MNEMONIC = 'vpackuswb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x67)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpackusdw_b:
    """vpackusdw"""
    MNEMONIC = 'vpackusdw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x2b)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmaddwd_b:
    """vpmaddwd"""
    MNEMONIC = 'vpmaddwd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf5)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpmaddubsw_b:
    """vpmaddubsw"""
    MNEMONIC = 'vpmaddubsw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00010
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x4)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vrcpps_rm:
    """vrcpps"""
    MNEMONIC = 'vrcpps'
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
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x53)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vrcpss_rvm:
    """vrcpss"""
    MNEMONIC = 'vrcpss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x53)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vrsqrtps_rm:
    """vrsqrtps"""
    MNEMONIC = 'vrsqrtps'
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
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x52)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vrsqrtss_rvm:
    """vrsqrtss"""
    MNEMONIC = 'vrsqrtss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x52)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vroundpd_rmi:
    """vroundpd"""
    MNEMONIC = 'vroundpd'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x9)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vroundps_rmi:
    """vroundps"""
    MNEMONIC = 'vroundps'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x8)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vroundsd_rvmi:
    """vroundsd"""
    MNEMONIC = 'vroundsd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64', 'imm8')

    def __init__(self, xmm1, xmm2, xmm_m64, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xb)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vroundss_rvmi:
    """vroundss"""
    MNEMONIC = 'vroundss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32', 'imm8')

    def __init__(self, xmm1, xmm2, xmm_m32, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32
        self.imm8 = imm8

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00011
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xa)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class vpsllw_c:
    """vpsllw"""
    MNEMONIC = 'vpsllw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf1)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsllw_d:
    """vpsllw"""
    MNEMONIC = 'vpsllw'
    FIELDS = ('xmm1', 'xmm2', 'imm8')

    def __init__(self, xmm1, xmm2, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.imm8 = imm8

    def encode(self, buf):
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = 0x6
        vvvv = self.xmm1.enc()
        rm = self.xmm2.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x71)
        reg = 0x6
        self.xmm2.encode_modrm(buf, reg)
        self.imm8.encode(buf)

class vpslld_c:
    """vpslld"""
    MNEMONIC = 'vpslld'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf2)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpslld_d:
    """vpslld"""
    MNEMONIC = 'vpslld'
    FIELDS = ('xmm1', 'xmm2', 'imm8')

    def __init__(self, xmm1, xmm2, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.imm8 = imm8

    def encode(self, buf):
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = 0x6
        vvvv = self.xmm1.enc()
        rm = self.xmm2.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x72)
        reg = 0x6
        self.xmm2.encode_modrm(buf, reg)
        self.imm8.encode(buf)

class vpsllq_c:
    """vpsllq"""
    MNEMONIC = 'vpsllq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf3)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsllq_d:
    """vpsllq"""
    MNEMONIC = 'vpsllq'
    FIELDS = ('xmm1', 'xmm2', 'imm8')

    def __init__(self, xmm1, xmm2, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.imm8 = imm8

    def encode(self, buf):
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = 0x6
        vvvv = self.xmm1.enc()
        rm = self.xmm2.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x73)
        reg = 0x6
        self.xmm2.encode_modrm(buf, reg)
        self.imm8.encode(buf)

class vpslld_g:
    """vpslld"""
    MNEMONIC = 'vpslld'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        ll = 0b00
        pp = 0b01
        mmm = 0b00001
        w = False
        bcast = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0xf2)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vpslld_f:
    """vpslld"""
    MNEMONIC = 'vpslld'
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
        ll = 0b00
        pp = 0b01
        mmm = 0b00001
        w = False
        bcast = False
        reg = 0x6
        vvvv = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x72)
        reg = 0x6
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, Some(16))
        self.imm8.encode(buf)

class vpsllq_g:
    """vpsllq"""
    MNEMONIC = 'vpsllq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        ll = 0b00
        pp = 0b01
        mmm = 0b00001
        w = True
        bcast = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0xf3)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vpsllq_f:
    """vpsllq"""
    MNEMONIC = 'vpsllq'
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
        ll = 0b00
        pp = 0b01
        mmm = 0b00001
        w = True
        bcast = False
        reg = 0x6
        vvvv = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x73)
        reg = 0x6
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, Some(16))
        self.imm8.encode(buf)

class vpsraw_c:
    """vpsraw"""
    MNEMONIC = 'vpsraw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xe1)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsraw_d:
    """vpsraw"""
    MNEMONIC = 'vpsraw'
    FIELDS = ('xmm1', 'xmm2', 'imm8')

    def __init__(self, xmm1, xmm2, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.imm8 = imm8

    def encode(self, buf):
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = 0x4
        vvvv = self.xmm1.enc()
        rm = self.xmm2.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x71)
        reg = 0x4
        self.xmm2.encode_modrm(buf, reg)
        self.imm8.encode(buf)

class vpsrad_c:
    """vpsrad"""
    MNEMONIC = 'vpsrad'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xe2)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsrad_d:
    """vpsrad"""
    MNEMONIC = 'vpsrad'
    FIELDS = ('xmm1', 'xmm2', 'imm8')

    def __init__(self, xmm1, xmm2, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.imm8 = imm8

    def encode(self, buf):
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = 0x4
        vvvv = self.xmm1.enc()
        rm = self.xmm2.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x72)
        reg = 0x4
        self.xmm2.encode_modrm(buf, reg)
        self.imm8.encode(buf)

class vpsrlw_c:
    """vpsrlw"""
    MNEMONIC = 'vpsrlw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xd1)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsrlw_d:
    """vpsrlw"""
    MNEMONIC = 'vpsrlw'
    FIELDS = ('xmm1', 'xmm2', 'imm8')

    def __init__(self, xmm1, xmm2, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.imm8 = imm8

    def encode(self, buf):
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = 0x2
        vvvv = self.xmm1.enc()
        rm = self.xmm2.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x71)
        reg = 0x2
        self.xmm2.encode_modrm(buf, reg)
        self.imm8.encode(buf)

class vpsrld_c:
    """vpsrld"""
    MNEMONIC = 'vpsrld'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xd2)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsrld_d:
    """vpsrld"""
    MNEMONIC = 'vpsrld'
    FIELDS = ('xmm1', 'xmm2', 'imm8')

    def __init__(self, xmm1, xmm2, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.imm8 = imm8

    def encode(self, buf):
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = 0x2
        vvvv = self.xmm1.enc()
        rm = self.xmm2.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x72)
        reg = 0x2
        self.xmm2.encode_modrm(buf, reg)
        self.imm8.encode(buf)

class vpsrlq_c:
    """vpsrlq"""
    MNEMONIC = 'vpsrlq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xd3)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsrlq_d:
    """vpsrlq"""
    MNEMONIC = 'vpsrlq'
    FIELDS = ('xmm1', 'xmm2', 'imm8')

    def __init__(self, xmm1, xmm2, imm8):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.imm8 = imm8

    def encode(self, buf):
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = 0x2
        vvvv = self.xmm1.enc()
        rm = self.xmm2.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x73)
        reg = 0x2
        self.xmm2.encode_modrm(buf, reg)
        self.imm8.encode(buf)

class vpsrad_g:
    """vpsrad"""
    MNEMONIC = 'vpsrad'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        ll = 0b00
        pp = 0b01
        mmm = 0b00001
        w = False
        bcast = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0xe2)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vpsrad_f:
    """vpsrad"""
    MNEMONIC = 'vpsrad'
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
        ll = 0b00
        pp = 0b01
        mmm = 0b00001
        w = False
        bcast = False
        reg = 0x4
        vvvv = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x72)
        reg = 0x4
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, Some(16))
        self.imm8.encode(buf)

class vpsraq_g:
    """vpsraq"""
    MNEMONIC = 'vpsraq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        ll = 0b00
        pp = 0b01
        mmm = 0b00001
        w = True
        bcast = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0xe2)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vpsraq_f:
    """vpsraq"""
    MNEMONIC = 'vpsraq'
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
        ll = 0b00
        pp = 0b01
        mmm = 0b00001
        w = True
        bcast = False
        reg = 0x4
        vvvv = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x72)
        reg = 0x4
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, Some(16))
        self.imm8.encode(buf)

class vpsrld_g:
    """vpsrld"""
    MNEMONIC = 'vpsrld'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        ll = 0b00
        pp = 0b01
        mmm = 0b00001
        w = False
        bcast = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0xd2)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vpsrld_f:
    """vpsrld"""
    MNEMONIC = 'vpsrld'
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
        ll = 0b00
        pp = 0b01
        mmm = 0b00001
        w = False
        bcast = False
        reg = 0x2
        vvvv = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x72)
        reg = 0x2
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, Some(16))
        self.imm8.encode(buf)

class vpsrlq_g:
    """vpsrlq"""
    MNEMONIC = 'vpsrlq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        ll = 0b00
        pp = 0b01
        mmm = 0b00001
        w = True
        bcast = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0xd3)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, Some(16))

class vpsrlq_f:
    """vpsrlq"""
    MNEMONIC = 'vpsrlq'
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
        ll = 0b00
        pp = 0b01
        mmm = 0b00001
        w = True
        bcast = False
        reg = 0x2
        vvvv = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = EvexPrefix.three_op(reg, vvvv, rm, ll, pp, mmm, w, bcast)
        prefix.encode(buf)
        buf.put1(0x73)
        reg = 0x2
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, Some(16))
        self.imm8.encode(buf)

class vsqrtss_b:
    """vsqrtss"""
    MNEMONIC = 'vsqrtss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x51)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vsqrtsd_b:
    """vsqrtsd"""
    MNEMONIC = 'vsqrtsd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x51)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vsqrtps_b:
    """vsqrtps"""
    MNEMONIC = 'vsqrtps'
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
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x51)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vsqrtpd_b:
    """vsqrtpd"""
    MNEMONIC = 'vsqrtpd'
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
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.two_op(reg, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x51)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vsubss_b:
    """vsubss"""
    MNEMONIC = 'vsubss'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m32')

    def __init__(self, xmm1, xmm2, xmm_m32):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m32 = xmm_m32

    def encode(self, buf):
        if isinstance(self.xmm_m32, Mem):
            xmm_m32 = self.xmm_m32
            trap_code = xmm_m32.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b10
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5c)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class vsubsd_b:
    """vsubsd"""
    MNEMONIC = 'vsubsd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m64')

    def __init__(self, xmm1, xmm2, xmm_m64):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m64 = xmm_m64

    def encode(self, buf):
        if isinstance(self.xmm_m64, Mem):
            xmm_m64 = self.xmm_m64
            trap_code = xmm_m64.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b11
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5c)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class vsubps_b:
    """vsubps"""
    MNEMONIC = 'vsubps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5c)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vsubpd_b:
    """vsubpd"""
    MNEMONIC = 'vsubpd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x5c)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsubb_b:
    """vpsubb"""
    MNEMONIC = 'vpsubb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf8)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsubw_b:
    """vpsubw"""
    MNEMONIC = 'vpsubw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf9)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsubd_b:
    """vpsubd"""
    MNEMONIC = 'vpsubd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xfa)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsubq_b:
    """vpsubq"""
    MNEMONIC = 'vpsubq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xfb)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsubsb_b:
    """vpsubsb"""
    MNEMONIC = 'vpsubsb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xe8)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsubsw_b:
    """vpsubsw"""
    MNEMONIC = 'vpsubsw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xe9)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsubusb_b:
    """vpsubusb"""
    MNEMONIC = 'vpsubusb'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xd8)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpsubusw_b:
    """vpsubusw"""
    MNEMONIC = 'vpsubusw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xd9)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vunpcklps_b:
    """vunpcklps"""
    MNEMONIC = 'vunpcklps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x14)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vunpcklpd_b:
    """vunpcklpd"""
    MNEMONIC = 'vunpcklpd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x14)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vunpckhps_b:
    """vunpckhps"""
    MNEMONIC = 'vunpckhps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x15)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpunpckhbw_b:
    """vpunpckhbw"""
    MNEMONIC = 'vpunpckhbw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x68)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpunpckhwd_b:
    """vpunpckhwd"""
    MNEMONIC = 'vpunpckhwd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x69)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpunpckhdq_b:
    """vpunpckhdq"""
    MNEMONIC = 'vpunpckhdq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x6a)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpunpckhqdq_b:
    """vpunpckhqdq"""
    MNEMONIC = 'vpunpckhqdq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x6d)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpunpcklwd_b:
    """vpunpcklwd"""
    MNEMONIC = 'vpunpcklwd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x61)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpunpcklbw_b:
    """vpunpcklbw"""
    MNEMONIC = 'vpunpcklbw'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x60)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpunpckldq_b:
    """vpunpckldq"""
    MNEMONIC = 'vpunpckldq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x62)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpunpcklqdq_b:
    """vpunpcklqdq"""
    MNEMONIC = 'vpunpcklqdq'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x6c)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vxorps_b:
    """vxorps"""
    MNEMONIC = 'vxorps'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b00
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x57)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vxorpd_b:
    """vxorpd"""
    MNEMONIC = 'vxorpd'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0x57)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class vpxor_b:
    """vpxor"""
    MNEMONIC = 'vpxor'
    FIELDS = ('xmm1', 'xmm2', 'xmm_m128')

    def __init__(self, xmm1, xmm2, xmm_m128):
        self.xmm1 = xmm1
        self.xmm2 = xmm2
        self.xmm_m128 = xmm_m128

    def encode(self, buf):
        if isinstance(self.xmm_m128, Mem):
            xmm_m128 = self.xmm_m128
            trap_code = xmm_m128.trap_code()
            if trap_code is not None:
                buf.add_trap(trap_code)
        len = 0b0
        pp = 0b01
        mmmmm = 0b00001
        w = False
        reg = self.xmm1.enc()
        vvvv = self.xmm2.enc()
        rm = self.xmm_m128.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xef)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)
