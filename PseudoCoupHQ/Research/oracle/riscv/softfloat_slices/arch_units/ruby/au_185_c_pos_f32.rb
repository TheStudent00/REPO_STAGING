# arch-unit 185  --  c  `+a`  lhs=float rhs=None
# symbol op_21   outcome LIFTED   1 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.jr ra                              integer    return
#
# answer: float, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_185_c_pos_f32(p0)
  # fa0: operand `a` (float) arrives in fa0 as a bit pattern
  v1 = ((p0) & 0xffffffff)
  # the answer is float, 32 bits
  ((v1) & 0xffffffff)
end
