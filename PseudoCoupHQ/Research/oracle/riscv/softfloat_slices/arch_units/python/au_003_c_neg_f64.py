# arch-unit 3  --  c  `-a`  lhs=double rhs=None
# symbol op_16   outcome WALK_REFUSED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fsgnjn.d fa0, fa0, fa0             float    bit-manipulation
#   c.jr ra                            integer  return
#
# answer: f64, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_003_c_neg_f64(p0):
    # fa0: operand `a` (double) arrives in fa0
    v1 = p0
    v2 = (((v1) & 0x7fffffffffffffff) | (((~(v1)) & 0xffffffffffffffff) & 0x8000000000000000))
    return v2
