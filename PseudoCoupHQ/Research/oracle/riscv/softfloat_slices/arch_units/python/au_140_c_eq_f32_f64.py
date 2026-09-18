# arch-unit 140  --  c  `a == b`  lhs=float rhs=double
# symbol op_484   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.s fa5, fa0                  float    emulation:f32_to_f64_rm0
#   feq.d a0, fa1, fa5                 float    emulation:f64_eq_rm0
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_140_c_eq_f32_f64(p0, p1):
    # fa0: operand `a` (float) arrives in fa0
    v1 = ((p0) & 0xffffffff)
    # fa1: operand `b` (double) arrives in fa1
    v2 = p1
    v3 = f32_to_f64_rm0(v1)
    v4 = f64_eq_rm0(v2, v3)
    return v4
