# arch-unit 126  --  c  `a && b`  lhs=double rhs=double
# symbol op_346   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fmv.d.x fa5, zero                  float    bit-manipulation
#   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
#   feq.d a1, fa1, fa5                 float    emulation:f64_eq_rm0
#   c.or a0, a1                        integer  operator:|
#   xori a0, a0, 0x1                   integer  operator:^
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_126_c_land_f64_f64(p0, p1):
    # fa0: operand `a` (double) arrives in fa0
    v1 = p0
    # fa1: operand `b` (double) arrives in fa1
    v2 = p1
    v3 = 0x0
    v4 = f64_eq_rm0(v1, v3)
    v5 = f64_eq_rm0(v2, v3)
    v6 = ((v4) | (v5))
    v7 = ((v6) ^ 0x1)
    return v7
