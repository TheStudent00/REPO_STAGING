// arch-unit 119  --  c  `a && b`  lhs=float rhs=float
// symbol op_339   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   feq.s a1, fa1, fa5                 float    emulation:f32_eq_rm0
//   c.or a0, a1                        integer  operator:|
//   xori a0, a0, 0x1                   integer  operator:^
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_119_c_land_f32_f32(p0, p1) {
  // fa0: operand `a` (float) arrives in fa0
  const v1 = ((p0) & 0xffffffffn);
  // fa1: operand `b` (float) arrives in fa1
  const v2 = ((p1) & 0xffffffffn);
  const v3 = ((0x0n) & 0xffffffffn);
  const v4 = AF.f32_eq_rm0(v1, v3);
  const v5 = AF.f32_eq_rm0(v2, v3);
  const v6 = ((v4) | (v5));
  const v7 = ((v6) ^ 0x1n);
  return v7;
}

module.exports = { au_119_c_land_f32_f32 };
