# arch-unit 448  --  go  `a >> b`  lhs=int64 rhs=uint64
# symbol main.op_212   outcome LIFTED   5 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sltiu t0, a1, 0x40                   integer    operator:< unsigned
#   c.addi t0, -0x1                      integer    operator:+
#   or t0, a1, t0                        integer    operator:|
#   sra a0, a0, t0                       integer    arithmetic right shift, written out in unsigned bit operations
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: int64, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_448_go_shr_i64_u64(p0, p1):
    # a0: operand `a` (int64) arrives in a0
    v1 = p0
    # a1: operand `b` (uint64) arrives in a1
    v2 = p1
    v3 = au_sltu(v2, 0x40)
    v4 = au_add(v3, 0xffffffffffffffff)
    v5 = au_or(v2, v4)
    v6 = au_sra(v1, v5)
    # the answer is int64, 64 bits
    return v6
