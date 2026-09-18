# arch-unit 133  --  c  `a == b`  lhs=int64_t rhs=double
# symbol op_472   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.l fa5, a0, dyn              float    emulation:i64_to_f64_rm0
#   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_133_c_eq_i64_f64(p0, p1):
    # a0: operand `a` (int64_t) arrives in a0
    v1 = p0
    # fa0: operand `b` (double) arrives in fa0
    v2 = p1
    v3 = i64_to_f64_rm0(v1)
    v4 = f64_eq_rm0(v2, v3)
    return v4
