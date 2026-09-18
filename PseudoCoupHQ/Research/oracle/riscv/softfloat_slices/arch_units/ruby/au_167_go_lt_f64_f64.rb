# arch-unit 167  --  go  `a < b`  lhs=float64 rhs=float64
# symbol main.op_556   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   flt.d a0, fa0, fa1                 float    emulation:f64_lt_rm0
#   jalr zero, 0x0(ra)                 integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_167_go_lt_f64_f64(p0, p1)
  # fa0: operand `a` (float64) arrives in fa0
  v1 = p0
  # fa1: operand `b` (float64) arrives in fa1
  v2 = p1
  v3 = f64_lt_rm0(v1, v2)
  v3
end
