# arch-unit 99  --  c  `a || b`  lhs=float rhs=float
# symbol op_303   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fmv.w.x fa5, zero                  float    bit-manipulation
#   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
#   feq.s a1, fa1, fa5                 float    emulation:f32_eq_rm0
#   c.and a0, a1                       integer  operator:&
#   xori a0, a0, 0x1                   integer  operator:^
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_099_c_lor_f32_f32(p0, p1):
    # fa0: operand `a` (float) arrives in fa0
    v1 = ((p0) & 0xffffffff)
    # fa1: operand `b` (float) arrives in fa1
    v2 = ((p1) & 0xffffffff)
    v3 = ((0x0) & 0xffffffff)
    v4 = f32_eq_rm0(v1, v3)
    v5 = f32_eq_rm0(v2, v3)
    v6 = ((v4) & (v5))
    v7 = ((v6) ^ 0x1)
    return v7
