# arch-unit 257  --  c  `a - b`  lhs=int32_t rhs=uint64_t
# symbol op_140   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.sub a0, a1                         integer    operator:-
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_257_c_sub_i32_u64(p0, p1):
    # a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
    v1 = au_sext32(p0)
    # a1: operand `b` (uint64_t) arrives in a1
    v2 = p1
    v3 = au_sub(v1, v2)
    # the answer is uint64_t, 64 bits
    return v3
