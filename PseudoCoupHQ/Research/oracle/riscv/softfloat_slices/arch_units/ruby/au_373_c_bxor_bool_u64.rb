# arch-unit 373  --  c  `a ^ b`  lhs=bool rhs=uint64_t
# symbol op_422   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.xor a0, a1                         integer    operator:^
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_373_c_bxor_bool_u64(p0, p1)
  # a0: operand `a` (bool) zero-extended to XLEN
  v1 = ((p0) & 0x1)
  # a1: operand `b` (uint64_t) arrives in a1
  v2 = p1
  v3 = au_xor(v1, v2)
  # the answer is uint64_t, 64 bits
  v3
end
