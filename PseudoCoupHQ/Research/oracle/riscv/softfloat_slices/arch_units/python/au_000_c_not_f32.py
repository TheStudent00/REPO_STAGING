# arch-unit 0  --  c  `!a`  lhs=float rhs=None
# symbol op_3   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fmv.w.x fa5, zero                  float    bit-manipulation
#   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_000_c_not_f32(p0):
    # fa0: operand `a` (float) arrives in fa0
    v1 = ((p0) & 0xffffffff)
    v2 = ((0x0) & 0xffffffff)
    v3 = f32_eq_rm0(v1, v2)
    return v3
