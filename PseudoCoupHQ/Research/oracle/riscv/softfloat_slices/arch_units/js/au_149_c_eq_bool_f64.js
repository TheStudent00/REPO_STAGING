// arch-unit 149  --  c  `a == b`  lhs=bool rhs=double
// symbol op_496   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
//   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_149_c_eq_bool_f64(p0, p1) {
  // a0: operand `a` (bool) zero-extended
  const v1 = ((p0) & 0x1n);
  // fa0: operand `b` (double) arrives in fa0
  const v2 = p1;
  const v3 = AF.ui32_to_f64_rm0(((v1) & 0xffffffffn));
  const v4 = AF.f64_eq_rm0(v2, v3);
  return v4;
}

module.exports = { au_149_c_eq_bool_f64 };
