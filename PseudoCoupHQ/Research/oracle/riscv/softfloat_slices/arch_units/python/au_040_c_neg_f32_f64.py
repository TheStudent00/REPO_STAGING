# arch-unit 40  --  c  `a - b`  lhs=float rhs=double
# symbol op_160   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.s fa5, fa0                  float    emulation:f32_to_f64_rm0
#   fsub.d fa0, fa5, fa1, dyn          float    emulation:f64_sub_rm0
#   c.jr ra                            integer  return
#
# answer: f64, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_040_c_neg_f32_f64(p0, p1):
    # fa0: operand `a` (float) arrives in fa0
    v1 = ((p0) & 0xffffffff)
    # fa1: operand `b` (double) arrives in fa1
    v2 = p1
    v3 = f32_to_f64_rm0(v1)
    v4 = f64_sub_rm0(v3, v2)
    return v4
