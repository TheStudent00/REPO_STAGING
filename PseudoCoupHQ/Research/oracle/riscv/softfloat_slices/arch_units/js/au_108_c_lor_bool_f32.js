// arch-unit 108  --  c  `a || b`  lhs=bool rhs=float
// symbol op_315   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a1, fa0, fa5                 float    emulation:f32_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   c.or a0, a1                        integer  operator:|
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_108_c_lor_bool_f32(p0, p1) {
  // a0: operand `a` (bool) zero-extended
  const v1 = ((p0) & 0x1n);
  // fa0: operand `b` (float) arrives in fa0
  const v2 = ((p1) & 0xffffffffn);
  const v3 = ((0x0n) & 0xffffffffn);
  const v4 = AF.f32_eq_rm0(v2, v3);
  const v5 = ((v4) ^ 0x1n);
  const v6 = ((v1) | (v5));
  return v6;
}

module.exports = { au_108_c_lor_bool_f32 };
