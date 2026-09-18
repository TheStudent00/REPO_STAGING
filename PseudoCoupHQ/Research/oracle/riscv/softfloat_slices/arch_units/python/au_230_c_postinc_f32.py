# arch-unit 230  --  c  `a++`  lhs=float rhs=None
# symbol op_93   outcome LIFTED   1 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.jr ra                              integer    return
#
# answer: float, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_230_c_postinc_f32(p0):
    # fa0: operand `a` (float) arrives in fa0 as a bit pattern
    v1 = ((p0) & 0xffffffff)
    # the answer is float, 32 bits
    return ((v1) & 0xffffffff)
