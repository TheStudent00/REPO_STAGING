# arch-unit 143  --  c  `a == b`  lhs=double rhs=int64_t
# symbol op_487   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.l fa5, a0, dyn              float    emulation:i64_to_f64_rm0
#   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_143_c_eq_f64_i64(p0, p1):
    # fa0: operand `a` (double) arrives in fa0
    v1 = p0
    # a0: operand `b` (int64_t) arrives in a0
    v2 = p1
    v3 = i64_to_f64_rm0(v2)
    v4 = f64_eq_rm0(v1, v3)
    return v4
