// arch-unit 47  --  c  `a - b`  lhs=double rhs=bool
// symbol op_167   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
//   fsub.d fa0, fa0, fa5, dyn          float    emulation:f64_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_047_c_neg_f64_bool(p0, p1) {
  // fa0: operand `a` (double) arrives in fa0
  const v1 = p0;
  // a0: operand `b` (bool) zero-extended
  const v2 = ((p1) & 0x1n);
  const v3 = AF.ui32_to_f64_rm0(((v2) & 0xffffffffn));
  const v4 = AF.f64_sub_rm0(v1, v3);
  return v4;
}

module.exports = { au_047_c_neg_f64_bool };
