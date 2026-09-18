// arch-unit 11  --  c  `a + b`  lhs=int32_t rhs=double
// symbol op_106   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.w fa5, a0                   float    emulation:i32_to_f64_rm0
//   fadd.d fa0, fa0, fa5, dyn          float    emulation:f64_add_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_011_c_add_i32_f64(p0, p1) {
  // a0: operand `a` (int32_t) sign-extended to XLEN
  const v1 = (((((p0) & 0xffffffffn) ^ 0x80000000n) - 0x80000000n) & 0xffffffffffffffffn);
  // fa0: operand `b` (double) arrives in fa0
  const v2 = p1;
  const v3 = AF.i32_to_f64_rm0(((v1) & 0xffffffffn));
  const v4 = AF.f64_add_rm0(v2, v3);
  return v4;
}

module.exports = { au_011_c_add_i32_f64 };
