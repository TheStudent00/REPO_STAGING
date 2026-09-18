# arch-unit 35  --  c  `a - b`  lhs=uint64_t rhs=double
# symbol op_154   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.lu fa5, a0, dyn             float    emulation:ui64_to_f64_rm0
#   fsub.d fa0, fa5, fa0, dyn          float    emulation:f64_sub_rm0
#   c.jr ra                            integer  return
#
# answer: f64, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_035_c_neg_u64_f64(p0, p1):
    # a0: operand `a` (uint64_t) arrives in a0
    v1 = p0
    # fa0: operand `b` (double) arrives in fa0
    v2 = p1
    v3 = ui64_to_f64_rm0(v1)
    v4 = f64_sub_rm0(v3, v2)
    return v4
