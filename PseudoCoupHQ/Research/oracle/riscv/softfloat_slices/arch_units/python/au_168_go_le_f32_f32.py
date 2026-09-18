# arch-unit 168  --  go  `a <= b`  lhs=float32 rhs=float32
# symbol main.op_585   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fle.s a0, fa0, fa1                 float    emulation:f32_le_rm0
#   jalr zero, 0x0(ra)                 integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_168_go_le_f32_f32(p0, p1):
    # fa0: operand `a` (float32) arrives in fa0
    v1 = ((p0) & 0xffffffff)
    # fa1: operand `b` (float32) arrives in fa1
    v2 = ((p1) & 0xffffffff)
    v3 = f32_le_rm0(v1, v2)
    return v3
