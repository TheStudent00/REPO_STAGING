# arch-unit 259  --  c  `a - b`  lhs=int64_t rhs=int32_t
# symbol op_144   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.sub a0, a1                         integer    operator:-
#   c.jr ra                              integer    return
#
# answer: int64_t, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_259_c_sub_i64_i32(p0, p1):
    # a0: operand `a` (int64_t) arrives in a0
    v1 = p0
    # a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
    v2 = au_sext32(p1)
    v3 = au_sub(v1, v2)
    # the answer is int64_t, 64 bits
    return v3
