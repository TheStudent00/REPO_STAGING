# arch-unit 147  --  c  `a == b`  lhs=double rhs=bool
# symbol op_491   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
#   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_147_c_eq_f64_bool(p0, p1):
    # fa0: operand `a` (double) arrives in fa0
    v1 = p0
    # a0: operand `b` (bool) zero-extended
    v2 = ((p1) & 0x1)
    v3 = ui32_to_f64_rm0(((v2) & 0xffffffff))
    v4 = f64_eq_rm0(v1, v3)
    return v4
