# arch-unit 44  --  c  `a - b`  lhs=double rhs=uint64_t
# symbol op_164   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.lu fa5, a0, dyn             float    emulation:ui64_to_f64_rm0
#   fsub.d fa0, fa0, fa5, dyn          float    emulation:f64_sub_rm0
#   c.jr ra                            integer  return
#
# answer: f64, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_044_c_neg_f64_u64(p0, p1):
    # fa0: operand `a` (double) arrives in fa0
    v1 = p0
    # a0: operand `b` (uint64_t) arrives in a0
    v2 = p1
    v3 = ui64_to_f64_rm0(v2)
    v4 = f64_sub_rm0(v1, v3)
    return v4
