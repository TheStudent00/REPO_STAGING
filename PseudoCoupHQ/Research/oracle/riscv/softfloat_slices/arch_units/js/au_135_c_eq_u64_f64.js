// arch-unit 135  --  c  `a == b`  lhs=uint64_t rhs=double
// symbol op_478   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.lu fa5, a0, dyn             float    emulation:ui64_to_f64_rm0
//   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_135_c_eq_u64_f64(p0, p1) {
  // a0: operand `a` (uint64_t) arrives in a0
  const v1 = p0;
  // fa0: operand `b` (double) arrives in fa0
  const v2 = p1;
  const v3 = AF.ui64_to_f64_rm0(v1);
  const v4 = AF.f64_eq_rm0(v2, v3);
  return v4;
}

module.exports = { au_135_c_eq_u64_f64 };
