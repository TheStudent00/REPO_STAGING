"""GENERATED — do not edit. Regenerate with transpile_vocab.py.

source        assembler.rs
source sha256 338def5b2c2f9e49cf138622f7423097395d9eeada913ad47ea7d50dcbda4a15
cranelift     unknown
transpiler    v1

Deterministic: same input -> byte-identical output.
"""

from vocab_support import *      # noqa: F401,F403

class cmpxchg16b_m:
    """cmpxchg16b"""
    MNEMONIC = 'cmpxchg16b'
    FIELDS = ('rax', 'rdx', 'rbx', 'rcx', 'm128')

    def __init__(self, rax, rdx, rbx, rcx, m128):
        self.rax = rax
        self.rdx = rdx
        self.rbx = rbx
        self.rcx = rcx
        self.m128 = m128

    def encode(self, buf):
        trap_code = self.m128.trap_code()
        if trap_code is not None:
            buf.add_trap(trap_code)
        uses_8bit = False
        w_bit = True
        digit = 0x1
        rex = self.m128.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xc7)
        reg = 0x1
        self.m128.encode_rex_suffixes(buf, reg, 0, None)

class cmpxchgb_mr:
    """cmpxchgb"""
    MNEMONIC = 'cmpxchgb'
    FIELDS = ('rm8', 'r8', 'al')

    def __init__(self, rm8, r8, al):
        self.rm8 = rm8
        self.r8 = r8
        self.al = al

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
        buf.put1(0x0f)
        buf.put1(0xb0)
        reg = self.r8.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class cmpxchgw_mr:
    """cmpxchgw"""
    MNEMONIC = 'cmpxchgw'
    FIELDS = ('rm16', 'r16', 'ax')

    def __init__(self, rm16, r16, ax):
        self.rm16 = rm16
        self.r16 = r16
        self.ax = ax

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
        buf.put1(0xb1)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmpxchgl_mr:
    """cmpxchgl"""
    MNEMONIC = 'cmpxchgl'
    FIELDS = ('rm32', 'r32', 'eax')

    def __init__(self, rm32, r32, eax):
        self.rm32 = rm32
        self.r32 = r32
        self.eax = eax

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
        buf.put1(0xb1)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmpxchgq_mr:
    """cmpxchgq"""
    MNEMONIC = 'cmpxchgq'
    FIELDS = ('rm64', 'r64', 'rax')

    def __init__(self, rm64, r64, rax):
        self.rm64 = rm64
        self.r64 = r64
        self.rax = rax

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
        buf.put1(0xb1)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cbtw_zo:
    """cbtw"""
    MNEMONIC = 'cbtw'
    FIELDS = ('ax',)

    def __init__(self, ax):
        self.ax = ax

    def encode(self, buf):
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        digit = 0
        dst = self.ax.enc()
        rex = RexPrefix.with_digit(digit, dst, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x98)

class cwtl_zo:
    """cwtl"""
    MNEMONIC = 'cwtl'
    FIELDS = ('eax',)

    def __init__(self, eax):
        self.eax = eax

    def encode(self, buf):
        uses_8bit = False
        w_bit = False
        digit = 0
        dst = self.eax.enc()
        rex = RexPrefix.with_digit(digit, dst, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x98)

class cltq_zo:
    """cltq"""
    MNEMONIC = 'cltq'
    FIELDS = ('rax',)

    def __init__(self, rax):
        self.rax = rax

    def encode(self, buf):
        uses_8bit = False
        w_bit = True
        digit = 0
        dst = self.rax.enc()
        rex = RexPrefix.with_digit(digit, dst, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x98)

class cwtd_zo:
    """cwtd"""
    MNEMONIC = 'cwtd'
    FIELDS = ('dx', 'ax')

    def __init__(self, dx, ax):
        self.dx = dx
        self.ax = ax

    def encode(self, buf):
        buf.put1(0x66)
        uses_8bit = False
        w_bit = False
        digit = 0
        dst = self.dx.enc()
        rex = RexPrefix.with_digit(digit, dst, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x99)

class cltd_zo:
    """cltd"""
    MNEMONIC = 'cltd'
    FIELDS = ('edx', 'eax')

    def __init__(self, edx, eax):
        self.edx = edx
        self.eax = eax

    def encode(self, buf):
        uses_8bit = False
        w_bit = False
        digit = 0
        dst = self.edx.enc()
        rex = RexPrefix.with_digit(digit, dst, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x99)

class cqto_zo:
    """cqto"""
    MNEMONIC = 'cqto'
    FIELDS = ('rdx', 'rax')

    def __init__(self, rdx, rax):
        self.rdx = rdx
        self.rax = rax

    def encode(self, buf):
        uses_8bit = False
        w_bit = True
        digit = 0
        dst = self.rdx.enc()
        rex = RexPrefix.with_digit(digit, dst, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x99)

class cmovaw_rm:
    """cmovaw"""
    MNEMONIC = 'cmovaw'
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
        buf.put1(0x47)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmoval_rm:
    """cmoval"""
    MNEMONIC = 'cmoval'
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
        buf.put1(0x47)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovaq_rm:
    """cmovaq"""
    MNEMONIC = 'cmovaq'
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
        buf.put1(0x47)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovaew_rm:
    """cmovaew"""
    MNEMONIC = 'cmovaew'
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
        buf.put1(0x43)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovael_rm:
    """cmovael"""
    MNEMONIC = 'cmovael'
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
        buf.put1(0x43)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovaeq_rm:
    """cmovaeq"""
    MNEMONIC = 'cmovaeq'
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
        buf.put1(0x43)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovbw_rm:
    """cmovbw"""
    MNEMONIC = 'cmovbw'
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
        buf.put1(0x42)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovbl_rm:
    """cmovbl"""
    MNEMONIC = 'cmovbl'
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
        buf.put1(0x42)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovbq_rm:
    """cmovbq"""
    MNEMONIC = 'cmovbq'
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
        buf.put1(0x42)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovbew_rm:
    """cmovbew"""
    MNEMONIC = 'cmovbew'
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
        buf.put1(0x46)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovbel_rm:
    """cmovbel"""
    MNEMONIC = 'cmovbel'
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
        buf.put1(0x46)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovbeq_rm:
    """cmovbeq"""
    MNEMONIC = 'cmovbeq'
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
        buf.put1(0x46)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovew_rm:
    """cmovew"""
    MNEMONIC = 'cmovew'
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
        buf.put1(0x44)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovel_rm:
    """cmovel"""
    MNEMONIC = 'cmovel'
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
        buf.put1(0x44)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmoveq_rm:
    """cmoveq"""
    MNEMONIC = 'cmoveq'
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
        buf.put1(0x44)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovgw_rm:
    """cmovgw"""
    MNEMONIC = 'cmovgw'
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
        buf.put1(0x4f)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovgl_rm:
    """cmovgl"""
    MNEMONIC = 'cmovgl'
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
        buf.put1(0x4f)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovgq_rm:
    """cmovgq"""
    MNEMONIC = 'cmovgq'
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
        buf.put1(0x4f)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovgew_rm:
    """cmovgew"""
    MNEMONIC = 'cmovgew'
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
        buf.put1(0x4d)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovgel_rm:
    """cmovgel"""
    MNEMONIC = 'cmovgel'
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
        buf.put1(0x4d)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovgeq_rm:
    """cmovgeq"""
    MNEMONIC = 'cmovgeq'
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
        buf.put1(0x4d)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovlw_rm:
    """cmovlw"""
    MNEMONIC = 'cmovlw'
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
        buf.put1(0x4c)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovll_rm:
    """cmovll"""
    MNEMONIC = 'cmovll'
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
        buf.put1(0x4c)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovlq_rm:
    """cmovlq"""
    MNEMONIC = 'cmovlq'
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
        buf.put1(0x4c)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovlew_rm:
    """cmovlew"""
    MNEMONIC = 'cmovlew'
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
        buf.put1(0x4e)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovlel_rm:
    """cmovlel"""
    MNEMONIC = 'cmovlel'
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
        buf.put1(0x4e)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovleq_rm:
    """cmovleq"""
    MNEMONIC = 'cmovleq'
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
        buf.put1(0x4e)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovnew_rm:
    """cmovnew"""
    MNEMONIC = 'cmovnew'
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
        buf.put1(0x45)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovnel_rm:
    """cmovnel"""
    MNEMONIC = 'cmovnel'
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
        buf.put1(0x45)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovneq_rm:
    """cmovneq"""
    MNEMONIC = 'cmovneq'
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
        buf.put1(0x45)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovnow_rm:
    """cmovnow"""
    MNEMONIC = 'cmovnow'
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
        buf.put1(0x41)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovnol_rm:
    """cmovnol"""
    MNEMONIC = 'cmovnol'
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
        buf.put1(0x41)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovnoq_rm:
    """cmovnoq"""
    MNEMONIC = 'cmovnoq'
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
        buf.put1(0x41)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovnpw_rm:
    """cmovnpw"""
    MNEMONIC = 'cmovnpw'
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
        buf.put1(0x4b)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovnpl_rm:
    """cmovnpl"""
    MNEMONIC = 'cmovnpl'
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
        buf.put1(0x4b)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovnpq_rm:
    """cmovnpq"""
    MNEMONIC = 'cmovnpq'
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
        buf.put1(0x4b)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovnsw_rm:
    """cmovnsw"""
    MNEMONIC = 'cmovnsw'
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
        buf.put1(0x49)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovnsl_rm:
    """cmovnsl"""
    MNEMONIC = 'cmovnsl'
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
        buf.put1(0x49)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovnsq_rm:
    """cmovnsq"""
    MNEMONIC = 'cmovnsq'
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
        buf.put1(0x49)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovow_rm:
    """cmovow"""
    MNEMONIC = 'cmovow'
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
        buf.put1(0x40)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovol_rm:
    """cmovol"""
    MNEMONIC = 'cmovol'
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
        buf.put1(0x40)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovoq_rm:
    """cmovoq"""
    MNEMONIC = 'cmovoq'
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
        buf.put1(0x40)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovpw_rm:
    """cmovpw"""
    MNEMONIC = 'cmovpw'
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
        buf.put1(0x4a)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovpl_rm:
    """cmovpl"""
    MNEMONIC = 'cmovpl'
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
        buf.put1(0x4a)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovpq_rm:
    """cmovpq"""
    MNEMONIC = 'cmovpq'
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
        buf.put1(0x4a)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmovsw_rm:
    """cmovsw"""
    MNEMONIC = 'cmovsw'
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
        buf.put1(0x48)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmovsl_rm:
    """cmovsl"""
    MNEMONIC = 'cmovsl'
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
        buf.put1(0x48)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmovsq_rm:
    """cmovsq"""
    MNEMONIC = 'cmovsq'
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
        buf.put1(0x48)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmpb_i:
    """cmpb"""
    MNEMONIC = 'cmpb'
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
        buf.put1(0x3c)
        self.imm8.encode(buf)

class cmpw_i:
    """cmpw"""
    MNEMONIC = 'cmpw'
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
        buf.put1(0x3d)
        self.imm16.encode(buf)

class cmpl_i:
    """cmpl"""
    MNEMONIC = 'cmpl'
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
        buf.put1(0x3d)
        self.imm32.encode(buf)

class cmpq_i:
    """cmpq"""
    MNEMONIC = 'cmpq'
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
        buf.put1(0x3d)
        self.imm32.encode(buf)

class cmpb_mi:
    """cmpb"""
    MNEMONIC = 'cmpb'
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
        buf.put1(0x80)
        reg = 0x7
        self.rm8.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class cmpw_mi:
    """cmpw"""
    MNEMONIC = 'cmpw'
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
        digit = 0x7
        rex = self.rm16.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x7
        self.rm16.encode_rex_suffixes(buf, reg, 2, None)
        self.imm16.encode(buf)

class cmpl_mi:
    """cmpl"""
    MNEMONIC = 'cmpl'
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
        digit = 0x7
        rex = self.rm32.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x7
        self.rm32.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class cmpq_mi:
    """cmpq"""
    MNEMONIC = 'cmpq'
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
        digit = 0x7
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x81)
        reg = 0x7
        self.rm64.encode_rex_suffixes(buf, reg, 4, None)
        self.imm32.encode(buf)

class cmpw_mi_sxb:
    """cmpw"""
    MNEMONIC = 'cmpw'
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
        buf.put1(0x83)
        reg = 0x7
        self.rm16.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class cmpl_mi_sxb:
    """cmpl"""
    MNEMONIC = 'cmpl'
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
        buf.put1(0x83)
        reg = 0x7
        self.rm32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class cmpq_mi_sxb:
    """cmpq"""
    MNEMONIC = 'cmpq'
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
        buf.put1(0x83)
        reg = 0x7
        self.rm64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class cmpb_mr:
    """cmpb"""
    MNEMONIC = 'cmpb'
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
        buf.put1(0x38)
        reg = self.r8.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class cmpw_mr:
    """cmpw"""
    MNEMONIC = 'cmpw'
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
        buf.put1(0x39)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmpl_mr:
    """cmpl"""
    MNEMONIC = 'cmpl'
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
        buf.put1(0x39)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmpq_mr:
    """cmpq"""
    MNEMONIC = 'cmpq'
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
        buf.put1(0x39)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmpb_rm:
    """cmpb"""
    MNEMONIC = 'cmpb'
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
        buf.put1(0x3a)
        reg = self.r8.enc()
        self.rm8.encode_rex_suffixes(buf, reg, 0, None)

class cmpw_rm:
    """cmpw"""
    MNEMONIC = 'cmpw'
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
        buf.put1(0x3b)
        reg = self.r16.enc()
        self.rm16.encode_rex_suffixes(buf, reg, 0, None)

class cmpl_rm:
    """cmpl"""
    MNEMONIC = 'cmpl'
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
        buf.put1(0x3b)
        reg = self.r32.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cmpq_rm:
    """cmpq"""
    MNEMONIC = 'cmpq'
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
        buf.put1(0x3b)
        reg = self.r64.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cmpss_a:
    """cmpss"""
    MNEMONIC = 'cmpss'
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
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xc2)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class cmpsd_a:
    """cmpsd"""
    MNEMONIC = 'cmpsd'
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
        buf.put1(0xF2)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xc2)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class cmpps_a:
    """cmpps"""
    MNEMONIC = 'cmpps'
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
        buf.put1(0xc2)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class cmppd_a:
    """cmppd"""
    MNEMONIC = 'cmppd'
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
        buf.put1(0xc2)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 1, None)
        self.imm8.encode(buf)

class cvtps2pd_a:
    """cvtps2pd"""
    MNEMONIC = 'cvtps2pd'
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
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x5a)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class cvttps2dq_a:
    """cvttps2dq"""
    MNEMONIC = 'cvttps2dq'
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
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m128.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x5b)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class cvtss2sd_a:
    """cvtss2sd"""
    MNEMONIC = 'cvtss2sd'
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
        buf.put1(0x5a)
        reg = self.xmm1.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class cvtss2si_a:
    """cvtss2si"""
    MNEMONIC = 'cvtss2si'
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
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.xmm_m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x2d)
        reg = self.r32.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class cvtss2si_aq:
    """cvtss2si"""
    MNEMONIC = 'cvtss2si'
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
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.xmm_m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x2d)
        reg = self.r64.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class cvttss2si_a:
    """cvttss2si"""
    MNEMONIC = 'cvttss2si'
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
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.xmm_m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x2c)
        reg = self.r32.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class cvttss2si_aq:
    """cvttss2si"""
    MNEMONIC = 'cvttss2si'
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
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.xmm_m32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x2c)
        reg = self.r64.enc()
        self.xmm_m32.encode_rex_suffixes(buf, reg, 0, None)

class cvtpd2ps_a:
    """cvtpd2ps"""
    MNEMONIC = 'cvtpd2ps'
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
        buf.put1(0x5a)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class cvttpd2dq_a:
    """cvttpd2dq"""
    MNEMONIC = 'cvttpd2dq'
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
        buf.put1(0xe6)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class cvtsd2ss_a:
    """cvtsd2ss"""
    MNEMONIC = 'cvtsd2ss'
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
        buf.put1(0x5a)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class cvtsd2si_a:
    """cvtsd2si"""
    MNEMONIC = 'cvtsd2si'
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
        buf.put1(0xF2)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.xmm_m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x2d)
        reg = self.r32.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class cvtsd2si_aq:
    """cvtsd2si"""
    MNEMONIC = 'cvtsd2si'
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
        buf.put1(0xF2)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.xmm_m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x2d)
        reg = self.r64.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class cvttsd2si_a:
    """cvttsd2si"""
    MNEMONIC = 'cvttsd2si'
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
        buf.put1(0xF2)
        uses_8bit = False
        w_bit = False
        reg = self.r32.enc()
        rex = self.xmm_m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x2c)
        reg = self.r32.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class cvttsd2si_aq:
    """cvttsd2si"""
    MNEMONIC = 'cvttsd2si'
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
        buf.put1(0xF2)
        uses_8bit = False
        w_bit = True
        reg = self.r64.enc()
        rex = self.xmm_m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x2c)
        reg = self.r64.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class cvtdq2ps_a:
    """cvtdq2ps"""
    MNEMONIC = 'cvtdq2ps'
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
        buf.put1(0x5b)
        reg = self.xmm1.enc()
        self.xmm_m128.encode_rex_suffixes(buf, reg, 0, None)

class cvtdq2pd_a:
    """cvtdq2pd"""
    MNEMONIC = 'cvtdq2pd'
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
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.xmm_m64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0xe6)
        reg = self.xmm1.enc()
        self.xmm_m64.encode_rex_suffixes(buf, reg, 0, None)

class cvtsi2ssl_a:
    """cvtsi2ssl"""
    MNEMONIC = 'cvtsi2ssl'
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
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.rm32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x2a)
        reg = self.xmm1.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cvtsi2ssq_a:
    """cvtsi2ssq"""
    MNEMONIC = 'cvtsi2ssq'
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
        buf.put1(0xF3)
        uses_8bit = False
        w_bit = True
        reg = self.xmm1.enc()
        rex = self.rm64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x2a)
        reg = self.xmm1.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class cvtsi2sdl_a:
    """cvtsi2sdl"""
    MNEMONIC = 'cvtsi2sdl'
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
        buf.put1(0xF2)
        uses_8bit = False
        w_bit = False
        reg = self.xmm1.enc()
        rex = self.rm32.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x2a)
        reg = self.xmm1.enc()
        self.rm32.encode_rex_suffixes(buf, reg, 0, None)

class cvtsi2sdq_a:
    """cvtsi2sdq"""
    MNEMONIC = 'cvtsi2sdq'
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
        buf.put1(0xF2)
        uses_8bit = False
        w_bit = True
        reg = self.xmm1.enc()
        rex = self.rm64.as_rex_prefix(reg, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0x0f)
        buf.put1(0x2a)
        reg = self.xmm1.enc()
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)

class callq_d:
    """callq"""
    MNEMONIC = 'callq'
    FIELDS = ('imm32',)

    def __init__(self, imm32):
        self.imm32 = imm32

    def encode(self, buf):
        buf.put1(0xe8)
        self.imm32.encode(buf)

class callq_m:
    """callq"""
    MNEMONIC = 'callq'
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
        digit = 0x2
        rex = self.rm64.as_rex_prefix(digit, w_bit, uses_8bit)
        rex.encode(buf)
        buf.put1(0xff)
        reg = 0x2
        self.rm64.encode_rex_suffixes(buf, reg, 0, None)
