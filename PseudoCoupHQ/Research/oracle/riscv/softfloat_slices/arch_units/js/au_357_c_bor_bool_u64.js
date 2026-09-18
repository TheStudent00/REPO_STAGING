// arch-unit 357  --  c  `a | b`  lhs=bool rhs=uint64_t
// symbol op_386   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_357_c_bor_bool_u64(p0, p1) {
  // a0: operand `a` (bool) zero-extended to XLEN
  const v1 = ((p0) & 0x1n);
  // a1: operand `b` (uint64_t) arrives in a1
  const v2 = p1;
  const v3 = AU.au_or(v1, v2);
  // the answer is uint64_t, 64 bits
  return v3;
}

module.exports = { au_357_c_bor_bool_u64 };
