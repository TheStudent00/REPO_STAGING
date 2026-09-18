# arch-unit 392  --  c  `a == b`  lhs=int32_t rhs=int64_t
# symbol op_463   outcome LIFTED   3 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.xor a0, a1                         integer    operator:^
#   sltiu a0, a0, 0x1                    integer    operator:< unsigned
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_392_c_eq_i32_i64(p0, p1):
    # a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
    v1 = au_sext32(p0)
    # a1: operand `b` (int64_t) arrives in a1
    v2 = p1
    v3 = au_xor(v1, v2)
    v4 = au_sltu(v3, 0x1)
    # the answer is int32_t, 32 bits
    return ((v4) & 0xffffffff)
