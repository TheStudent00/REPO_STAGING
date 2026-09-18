# arch-unit 485  --  go  `a > b`  lhs=int64 rhs=int64
# symbol main.op_607   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   slt a0, a1, a0                       integer    operator:< signed
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: bool, 1 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_485_go_gt_i64_i64(p0, p1):
    # a0: operand `a` (int64) arrives in a0
    v1 = p0
    # a1: operand `b` (int64) arrives in a1
    v2 = p1
    v3 = au_slt(v2, v1)
    # the answer is bool, 1 bits
    return ((v3) & 0x1)
