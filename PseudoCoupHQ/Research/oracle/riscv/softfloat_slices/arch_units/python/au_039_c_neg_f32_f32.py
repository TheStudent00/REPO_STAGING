# arch-unit 39  --  c  `a - b`  lhs=float rhs=float
# symbol op_159   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fsub.s fa0, fa0, fa1, dyn          float    emulation:f32_sub_rm0
#   c.jr ra                            integer  return
#
# answer: f32, 32 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_039_c_neg_f32_f32(p0, p1):
    # fa0: operand `a` (float) arrives in fa0
    v1 = ((p0) & 0xffffffff)
    # fa1: operand `b` (float) arrives in fa1
    v2 = ((p1) & 0xffffffff)
    v3 = f32_sub_rm0(v1, v2)
    return ((v3) & 0xffffffff)
