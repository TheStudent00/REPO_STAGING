// arch-unit 6  --  c  `++a`  lhs=float rhs=None
// symbol op_39   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fli.s fa5, 1.0                     float    bit-manipulation
//   fadd.s fa0, fa0, fa5, dyn          float    emulation:f32_add_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_006_c_preinc_f32(p0) {
  // fa0: operand `a` (float) arrives in fa0
  const v1 = ((p0) & 0xffffffffn);
  const v2 = 0x3f800000n;
  const v3 = AF.f32_add_rm0(v1, v2);
  return ((v3) & 0xffffffffn);
}

module.exports = { au_006_c_preinc_f32 };
