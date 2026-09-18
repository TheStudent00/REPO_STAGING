// arch-unit 93  --  c  `a || b`  lhs=int64_t rhs=double
// symbol op_292   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                  integer  operator:<
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   c.or a0, a1                        integer  operator:|
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_093_c_lor_i64_f64(p0, p1) {
  // a0: operand `a` (int64_t) arrives in a0
  const v1 = p0;
  // fa0: operand `b` (double) arrives in fa0
  const v2 = p1;
  const v3 = (((0x0n) < (v1)) ? 1n : 0n);
  const v4 = 0x0n;
  const v5 = AF.f64_eq_rm0(v2, v4);
  const v6 = ((v5) ^ 0x1n);
  const v7 = ((v3) | (v6));
  return v7;
}

module.exports = { au_093_c_lor_i64_f64 };
