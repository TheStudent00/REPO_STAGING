# arch-unit 205  --  c  `__alignof__ a`  lhs=uint64_t rhs=None
# symbol op_56   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.li a0, 0x8                         integer    constant
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_205_c_alignof_gnu2_u64(p0)
  # a0: operand `a` (uint64_t) arrives in a0
  v1 = p0
  v2 = 0x8
  # the answer is uint64_t, 64 bits
  v2
end
