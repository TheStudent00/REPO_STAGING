# arch-unit 413  --  go  `+a`  lhs=float64 rhs=None
# symbol main.op_4   outcome LIFTED   1 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: float64, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_413_go_pos_f64(p0)
  # fa0: operand `a` (float64) arrives in fa0 as a bit pattern
  v1 = p0
  # the answer is float64, 64 bits
  v1
end
