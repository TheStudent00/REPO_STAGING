// arch-unit 62  --  c  `a * b`  lhs=double rhs=int32_t
// symbol op_198   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.w fa5, a0                   float    emulation:i32_to_f64_rm0
//   fmul.d fa0, fa0, fa5, dyn          float    emulation:f64_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_062_c_mul_f64_i32(p0, p1) {
  // fa0: operand `a` (double) arrives in fa0
  const v1 = p0;
  // a0: operand `b` (int32_t) sign-extended to XLEN
  const v2 = (((((p1) & 0xffffffffn) ^ 0x80000000n) - 0x80000000n) & 0xffffffffffffffffn);
  const v3 = AF.i32_to_f64_rm0(((v2) & 0xffffffffn));
  const v4 = AF.f64_mul_rm0(v1, v3);
  return v4;
}

module.exports = { au_062_c_mul_f64_i32 };
