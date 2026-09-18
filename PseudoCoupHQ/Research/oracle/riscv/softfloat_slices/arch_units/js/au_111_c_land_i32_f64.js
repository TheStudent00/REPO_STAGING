// arch-unit 111  --  c  `a && b`  lhs=int32_t rhs=double
// symbol op_322   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                  integer  operator:<
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   c.and a0, a1                       integer  operator:&
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_111_c_land_i32_f64(p0, p1) {
  // a0: operand `a` (int32_t) sign-extended to XLEN
  const v1 = (((((p0) & 0xffffffffn) ^ 0x80000000n) - 0x80000000n) & 0xffffffffffffffffn);
  // fa0: operand `b` (double) arrives in fa0
  const v2 = p1;
  const v3 = (((0x0n) < (v1)) ? 1n : 0n);
  const v4 = 0x0n;
  const v5 = AF.f64_eq_rm0(v2, v4);
  const v6 = ((v5) ^ 0x1n);
  const v7 = ((v3) & (v6));
  return v7;
}

module.exports = { au_111_c_land_i32_f64 };
