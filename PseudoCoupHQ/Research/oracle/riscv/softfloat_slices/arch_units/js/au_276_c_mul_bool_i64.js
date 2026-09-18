// arch-unit 276  --  c  `a * b`  lhs=bool rhs=int64_t
// symbol op_205   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   czero.eqz a0, a1, a0                 integer    conditional select
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_276_c_mul_bool_i64(p0, p1) {
  // a0: operand `a` (bool) zero-extended to XLEN
  const v1 = ((p0) & 0x1n);
  // a1: operand `b` (int64_t) arrives in a1
  const v2 = p1;
  const v3 = AU.au_czeqz(v2, v1);
  // the answer is int64_t, 64 bits
  return v3;
}

module.exports = { au_276_c_mul_bool_i64 };
