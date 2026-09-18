# arch-unit 131  --  c  `a == b`  lhs=int32_t rhs=double
# symbol op_466   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.w fa5, a0                   float    emulation:i32_to_f64_rm0
#   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_131_c_eq_i32_f64(p0, p1):
    # a0: operand `a` (int32_t) sign-extended to XLEN
    v1 = (((((p0) & 0xffffffff) ^ 0x80000000) - 0x80000000) & 0xffffffffffffffff)
    # fa0: operand `b` (double) arrives in fa0
    v2 = p1
    v3 = i32_to_f64_rm0(((v1) & 0xffffffff))
    v4 = f64_eq_rm0(v2, v3)
    return v4
