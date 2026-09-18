# arch-unit 150  --  go  `-a`  lhs=float32 rhs=None
# symbol main.op_9   outcome WALK_REFUSED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fsgnjn.s fa0, fa0, fa0             float    bit-manipulation
#   jalr zero, 0x0(ra)                 integer  return
#
# answer: f32, 32 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_150_go_neg_f32(p0):
    # fa0: operand `a` (float32) arrives in fa0
    v1 = ((p0) & 0xffffffff)
    v2 = (((v1) & 0x7fffffff) | (((~(v1)) & 0xffffffffffffffff) & 0x80000000))
    return ((v2) & 0xffffffff)
