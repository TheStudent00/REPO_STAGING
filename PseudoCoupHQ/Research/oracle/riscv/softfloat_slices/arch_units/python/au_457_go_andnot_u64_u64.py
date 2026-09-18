# arch-unit 457  --  go  `a &^ b`  lhs=uint64 rhs=uint64
# symbol main.op_290   outcome LIFTED   3 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   xori t6, a1, -0x1                    integer    operator:^
#   and a0, a0, t6                       integer    operator:&
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: uint64, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_457_go_andnot_u64_u64(p0, p1):
    # a0: operand `a` (uint64) arrives in a0
    v1 = p0
    # a1: operand `b` (uint64) arrives in a1
    v2 = p1
    v3 = au_xor(v2, 0xffffffffffffffff)
    v4 = au_and(v1, v3)
    # the answer is uint64, 64 bits
    return v4
