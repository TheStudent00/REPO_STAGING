# arch-unit 266  --  c  `a - b`  lhs=uint64_t rhs=bool
# symbol op_155   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.sub a0, a1                         integer    operator:-
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_266_c_sub_u64_bool(p0, p1)
  # a0: operand `a` (uint64_t) arrives in a0
  v1 = p0
  # a1: operand `b` (bool) zero-extended to XLEN
  v2 = ((p1) & 0x1)
  v3 = au_sub(v1, v2)
  # the answer is uint64_t, 64 bits
  v3
end
