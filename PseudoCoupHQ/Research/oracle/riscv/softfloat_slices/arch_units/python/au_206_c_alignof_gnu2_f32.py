# arch-unit 206  --  c  `__alignof__ a`  lhs=float rhs=None
# symbol op_57   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.li a0, 0x4                         integer    constant
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_206_c_alignof_gnu2_f32(p0):
    # fa0: operand `a` (float) arrives in fa0 as a bit pattern
    v1 = ((p0) & 0xffffffff)
    v2 = 0x4
    # the answer is uint64_t, 64 bits
    return v2
