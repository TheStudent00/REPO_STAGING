// arch-unit 169  --  go  `a <= b`  lhs=float64 rhs=float64
// symbol main.op_592   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fle.d a0, fa0, fa1                 float    emulation:f64_le_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_169_go_le_f64_f64(p0, p1) {
  // fa0: operand `a` (float64) arrives in fa0
  const v1 = p0;
  // fa1: operand `b` (float64) arrives in fa1
  const v2 = p1;
  const v3 = AF.f64_le_rm0(v1, v2);
  return v3;
}

module.exports = { au_169_go_le_f64_f64 };
