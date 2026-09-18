// arch-unit 159  --  go  `a + b`  lhs=float64 rhs=float64
// symbol main.op_340   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fadd.d fa0, fa0, fa1, rne          float    emulation:f64_add_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_159_go_add_f64_f64(p0, p1) {
  // fa0: operand `a` (float64) arrives in fa0
  const v1 = p0;
  // fa1: operand `b` (float64) arrives in fa1
  const v2 = p1;
  const v3 = AF.f64_add_rm0(v1, v2);
  return v3;
}

module.exports = { au_159_go_add_f64_f64 };
