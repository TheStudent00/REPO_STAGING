# arch-unit 217  --  c  `_Alignof a`  lhs=uint64_t rhs=None
# symbol op_80   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.li a0, 0x8                         integer    constant
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_217_c_alignof_c11_u64(p0)
  # a0: operand `a` (uint64_t) arrives in a0
  v1 = p0
  v2 = 0x8
  # the answer is uint64_t, 64 bits
  v2
end
