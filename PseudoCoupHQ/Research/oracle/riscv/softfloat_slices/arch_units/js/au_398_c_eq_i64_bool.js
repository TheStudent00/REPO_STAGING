// arch-unit 398  --  c  `a == b`  lhs=int64_t rhs=bool
// symbol op_473   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_398_c_eq_i64_bool(p0, p1) {
  // a0: operand `a` (int64_t) arrives in a0
  const v1 = p0;
  // a1: operand `b` (bool) zero-extended to XLEN
  const v2 = ((p1) & 0x1n);
  const v3 = AU.au_xor(v1, v2);
  const v4 = AU.au_sltu(v3, 0x1n);
  // the answer is int32_t, 32 bits
  return ((v4) & 0xffffffffn);
}

module.exports = { au_398_c_eq_i64_bool };
