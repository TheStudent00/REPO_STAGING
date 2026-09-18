# arch-unit 231  --  c  `a++`  lhs=double rhs=None
# symbol op_94   outcome LIFTED   1 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.jr ra                              integer    return
#
# answer: double, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_231_c_postinc_f64(p0):
    # fa0: operand `a` (double) arrives in fa0 as a bit pattern
    v1 = p0
    # the answer is double, 64 bits
    return v1
