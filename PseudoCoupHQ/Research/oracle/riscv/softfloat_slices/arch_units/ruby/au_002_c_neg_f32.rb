# arch-unit 2  --  c  `-a`  lhs=float rhs=None
# symbol op_15   outcome WALK_REFUSED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fsgnjn.s fa0, fa0, fa0             float    bit-manipulation
#   c.jr ra                            integer  return
#
# answer: f32, 32 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_002_c_neg_f32(p0)
  # fa0: operand `a` (float) arrives in fa0
  v1 = ((p0) & 0xffffffff)
  v2 = (((v1) & 0x7fffffff) | (((~(v1)) & 0xffffffffffffffff) & 0x80000000))
  ((v2) & 0xffffffff)
end
