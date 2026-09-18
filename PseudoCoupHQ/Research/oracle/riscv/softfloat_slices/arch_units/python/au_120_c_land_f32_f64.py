# arch-unit 120  --  c  `a && b`  lhs=float rhs=double
# symbol op_340   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fmv.w.x fa5, zero                  float    bit-manipulation
#   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
#   fmv.d.x fa5, zero                  float    bit-manipulation
#   feq.d a1, fa1, fa5                 float    emulation:f64_eq_rm0
#   c.or a0, a1                        integer  operator:|
#   xori a0, a0, 0x1                   integer  operator:^
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_120_c_land_f32_f64(p0, p1):
    # fa0: operand `a` (float) arrives in fa0
    v1 = ((p0) & 0xffffffff)
    # fa1: operand `b` (double) arrives in fa1
    v2 = p1
    v3 = ((0x0) & 0xffffffff)
    v4 = f32_eq_rm0(v1, v3)
    v5 = 0x0
    v6 = f64_eq_rm0(v2, v5)
    v7 = ((v4) | (v6))
    v8 = ((v7) ^ 0x1)
    return v8
