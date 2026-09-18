# arch-unit 69  --  c  `a * b`  lhs=bool rhs=double
# symbol op_208   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
#   fmul.d fa0, fa0, fa5, dyn          float    emulation:f64_mul_rm0
#   c.jr ra                            integer  return
#
# answer: f64, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_069_c_mul_bool_f64(p0, p1):
    # a0: operand `a` (bool) zero-extended
    v1 = ((p0) & 0x1)
    # fa0: operand `b` (double) arrives in fa0
    v2 = p1
    v3 = ui32_to_f64_rm0(((v1) & 0xffffffff))
    v4 = f64_mul_rm0(v2, v3)
    return v4
