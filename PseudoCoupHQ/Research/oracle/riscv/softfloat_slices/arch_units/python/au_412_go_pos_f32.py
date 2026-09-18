# arch-unit 412  --  go  `+a`  lhs=float32 rhs=None
# symbol main.op_3   outcome LIFTED   1 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: float32, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_412_go_pos_f32(p0):
    # fa0: operand `a` (float32) arrives in fa0 as a bit pattern
    v1 = ((p0) & 0xffffffff)
    # the answer is float32, 32 bits
    return ((v1) & 0xffffffff)
