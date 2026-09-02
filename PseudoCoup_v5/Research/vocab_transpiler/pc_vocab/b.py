"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class bsfw_rm:
    """bsfw"""
    MNEMONIC = 'bsfw'
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
        buf.put1(0xbc)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class bsfl_rm:
    """bsfl"""
    MNEMONIC = 'bsfl'
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
        buf.put1(0xbc)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class bsfq_rm:
    """bsfq"""
    MNEMONIC = 'bsfq'
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
        buf.put1(0xbc)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class bsrw_rm:
    """bsrw"""
    MNEMONIC = 'bsrw'
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
        buf.put1(0xbd)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class bsrl_rm:
    """bsrl"""
    MNEMONIC = 'bsrl'
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
        buf.put1(0xbd)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class bsrq_rm:
    """bsrq"""
    MNEMONIC = 'bsrq'
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
        buf.put1(0xbd)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class btw_mr:
    """btw"""
    MNEMONIC = 'btw'
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
        buf.put1(0x0f)
        buf.put1(0xa3)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class btl_mr:
    """btl"""
    MNEMONIC = 'btl'
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
        buf.put1(0x0f)
        buf.put1(0xa3)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class btq_mr:
    """btq"""
    MNEMONIC = 'btq'
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
        buf.put1(0x0f)
        buf.put1(0xa3)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class btw_mi:
    """btw"""
    MNEMONIC = 'btw'
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
        buf.put1(0x0f)
        buf.put1(0xba)
        reg = 0x4
        self.rm16.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class btl_mi:
    """btl"""
    MNEMONIC = 'btl'
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
        buf.put1(0x0f)
        buf.put1(0xba)
        reg = 0x4
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class btq_mi:
    """btq"""
    MNEMONIC = 'btq'
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
        buf.put1(0x0f)
        buf.put1(0xba)
        reg = 0x4
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class bswapl_o:
    """bswapl"""
    MNEMONIC = 'bswapl'
    FIELDS = ('r32',)

    def __init__(self, r32):
        self.r32 = r32

    def encode(self, buf):
        uses_8bit = False
        w_bit = False
        dst = self.r32.enc()
        rex = RexPrefix.one_op(dst, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        low_bits = self.r32.enc() & 0b111
        buf.put1(0xc8 | low_bits)

class bswapq_o:
    """bswapq"""
    MNEMONIC = 'bswapq'
    FIELDS = ('r64',)

    def __init__(self, r64):
        self.r64 = r64

    def encode(self, buf):
        uses_8bit = False
        w_bit = True
        dst = self.r64.enc()
        rex = RexPrefix.one_op(dst, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        low_bits = self.r64.enc() & 0b111
        buf.put1(0xc8 | low_bits)

class blsrl_vm:
    """blsrl"""
    MNEMONIC = 'blsrl'
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
        len = 0b0
        pp = 0b00
        mmmmm = 0b00010
        w = False
        reg = 0x1
        vvvv = self.r32.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf3)
        reg = 0x1
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class blsrq_vm:
    """blsrq"""
    MNEMONIC = 'blsrq'
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
        len = 0b0
        pp = 0b00
        mmmmm = 0b00010
        w = True
        reg = 0x1
        vvvv = self.r64.enc()
        rm = self.rm64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf3)
        reg = 0x1
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class blsmskl_vm:
    """blsmskl"""
    MNEMONIC = 'blsmskl'
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
        len = 0b0
        pp = 0b00
        mmmmm = 0b00010
        w = False
        reg = 0x2
        vvvv = self.r32.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf3)
        reg = 0x2
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class blsmskq_vm:
    """blsmskq"""
    MNEMONIC = 'blsmskq'
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
        len = 0b0
        pp = 0b00
        mmmmm = 0b00010
        w = True
        reg = 0x2
        vvvv = self.r64.enc()
        rm = self.rm64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf3)
        reg = 0x2
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class blsil_vm:
    """blsil"""
    MNEMONIC = 'blsil'
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
        len = 0b0
        pp = 0b00
        mmmmm = 0b00010
        w = False
        reg = 0x3
        vvvv = self.r32.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf3)
        reg = 0x3
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class blsiq_vm:
    """blsiq"""
    MNEMONIC = 'blsiq'
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
        len = 0b0
        pp = 0b00
        mmmmm = 0b00010
        w = True
        reg = 0x3
        vvvv = self.r64.enc()
        rm = self.rm64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf3)
        reg = 0x3
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class bzhil_rmv:
    """bzhil"""
    MNEMONIC = 'bzhil'
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
        pp = 0b00
        mmmmm = 0b00010
        w = False
        reg = self.r32a.enc()
        vvvv = self.r32b.enc()
        rm = self.rm32.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf5)
        reg = self.r32a.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class bzhiq_rmv:
    """bzhiq"""
    MNEMONIC = 'bzhiq'
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
        pp = 0b00
        mmmmm = 0b00010
        w = True
        reg = self.r64a.enc()
        vvvv = self.r64b.enc()
        rm = self.rm64.encode_bx_regs()
        prefix = VexPrefix.three_op(reg, vvvv, rm, len, pp, mmmmm, w)
        prefix.encode(buf)
        buf.put1(0xf5)
        reg = self.r64a.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class blendvps_rm0:
    """blendvps"""
    MNEMONIC = 'blendvps'
    FIELDS = ('xmm1', 'xmm_m128', 'xmm0')

    def __init__(self, xmm1, xmm_m128, xmm0):
        self.xmm1 = xmm1
        self.xmm_m128 = xmm_m128
        self.xmm0 = xmm0

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
        buf.put1(0x38)
        buf.put1(0x14)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class blendvpd_rm0:
    """blendvpd"""
    MNEMONIC = 'blendvpd'
    FIELDS = ('xmm1', 'xmm_m128', 'xmm0')

    def __init__(self, xmm1, xmm_m128, xmm0):
        self.xmm1 = xmm1
        self.xmm_m128 = xmm_m128
        self.xmm0 = xmm0

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
        buf.put1(0x38)
        buf.put1(0x15)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)
