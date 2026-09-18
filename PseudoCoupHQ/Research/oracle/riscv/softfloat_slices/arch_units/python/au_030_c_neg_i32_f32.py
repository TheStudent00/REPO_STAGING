# arch-unit 30  --  c  `a - b`  lhs=int32_t rhs=float
# symbol op_141   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.s.w fa5, a0, dyn              float    emulation:i32_to_f32_rm0
#   fsub.s fa0, fa5, fa0, dyn          float    emulation:f32_sub_rm0
#   c.jr ra                            integer  return
#
# answer: f32, 32 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_030_c_neg_i32_f32(p0, p1):
    # a0: operand `a` (int32_t) sign-extended to XLEN
    v1 = (((((p0) & 0xffffffff) ^ 0x80000000) - 0x80000000) & 0xffffffffffffffff)
    # fa0: operand `b` (float) arrives in fa0
    v2 = ((p1) & 0xffffffff)
    v3 = i32_to_f32_rm0(((v1) & 0xffffffff))
    v4 = f32_sub_rm0(v3, v2)
    return ((v4) & 0xffffffff)
