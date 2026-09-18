# arch-unit 136  --  c  `a == b`  lhs=float rhs=int32_t
# symbol op_480   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.s.w fa5, a0, dyn              float    emulation:i32_to_f32_rm0
#   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_136_c_eq_f32_i32(p0, p1):
    # fa0: operand `a` (float) arrives in fa0
    v1 = ((p0) & 0xffffffff)
    # a0: operand `b` (int32_t) sign-extended to XLEN
    v2 = (((((p1) & 0xffffffff) ^ 0x80000000) - 0x80000000) & 0xffffffffffffffff)
    v3 = i32_to_f32_rm0(((v2) & 0xffffffff))
    v4 = f32_eq_rm0(v1, v3)
    return v4
