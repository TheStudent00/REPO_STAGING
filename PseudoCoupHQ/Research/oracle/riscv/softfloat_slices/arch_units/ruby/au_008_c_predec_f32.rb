# arch-unit 8  --  c  `--a`  lhs=float rhs=None
# symbol op_45   outcome WALK_REFUSED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fli.s fa5, -1.0                    float    bit-manipulation
#   fadd.s fa0, fa0, fa5, dyn          float    emulation:f32_add_rm0
#   c.jr ra                            integer  return
#
# answer: f32, 32 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_008_c_predec_f32(p0)
  # fa0: operand `a` (float) arrives in fa0
  v1 = ((p0) & 0xffffffff)
  v2 = 0xbf800000
  v3 = f32_add_rm0(v1, v2)
  ((v3) & 0xffffffff)
end
