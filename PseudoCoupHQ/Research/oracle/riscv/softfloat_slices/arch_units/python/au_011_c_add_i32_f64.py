# arch-unit 11  --  c  `a + b`  lhs=int32_t rhs=double
# symbol op_106   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.w fa5, a0                   float    emulation:i32_to_f64_rm0
#   fadd.d fa0, fa0, fa5, dyn          float    emulation:f64_add_rm0
#   c.jr ra                            integer  return
#
# answer: f64, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_011_c_add_i32_f64(p0, p1):
    # a0: operand `a` (int32_t) sign-extended to XLEN
    v1 = (((((p0) & 0xffffffff) ^ 0x80000000) - 0x80000000) & 0xffffffffffffffff)
    # fa0: operand `b` (double) arrives in fa0
    v2 = p1
    v3 = i32_to_f64_rm0(((v1) & 0xffffffff))
    v4 = f64_add_rm0(v2, v3)
    return v4
