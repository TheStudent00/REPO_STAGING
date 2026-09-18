# arch-unit 208  --  c  `__alignof__ a`  lhs=bool rhs=None
# symbol op_59   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.li a0, 0x1                         integer    constant
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_208_c_alignof_gnu2_bool(p0)
  # a0: operand `a` (bool) zero-extended to XLEN
  v1 = ((p0) & 0x1)
  v2 = 0x1
  # the answer is uint64_t, 64 bits
  v2
end
