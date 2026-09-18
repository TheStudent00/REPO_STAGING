# arch-unit 62  --  c  `a * b`  lhs=double rhs=int32_t
# symbol op_198   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.w fa5, a0                   float    emulation:i32_to_f64_rm0
#   fmul.d fa0, fa0, fa5, dyn          float    emulation:f64_mul_rm0
#   c.jr ra                            integer  return
#
# answer: f64, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_062_c_mul_f64_i32(p0, p1):
    # fa0: operand `a` (double) arrives in fa0
    v1 = p0
    # a0: operand `b` (int32_t) sign-extended to XLEN
    v2 = (((((p1) & 0xffffffff) ^ 0x80000000) - 0x80000000) & 0xffffffffffffffff)
    v3 = i32_to_f64_rm0(((v2) & 0xffffffff))
    v4 = f64_mul_rm0(v1, v3)
    return v4
