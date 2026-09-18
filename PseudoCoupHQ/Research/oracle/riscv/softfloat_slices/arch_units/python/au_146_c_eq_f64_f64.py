# arch-unit 146  --  c  `a == b`  lhs=double rhs=double
# symbol op_490   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   feq.d a0, fa0, fa1                 float    emulation:f64_eq_rm0
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_146_c_eq_f64_f64(p0, p1):
    # fa0: operand `a` (double) arrives in fa0
    v1 = p0
    # fa1: operand `b` (double) arrives in fa1
    v2 = p1
    v3 = f64_eq_rm0(v1, v2)
    return v3
