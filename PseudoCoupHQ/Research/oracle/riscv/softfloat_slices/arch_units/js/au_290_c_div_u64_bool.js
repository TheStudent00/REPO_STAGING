// arch-unit 290  --  c  `a / b`  lhs=uint64_t rhs=bool
// symbol op_227   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_290_c_div_u64_bool(p0, p1) {
  // a0: operand `a` (uint64_t) arrives in a0
  const v1 = p0;
  // a1: operand `b` (bool) zero-extended to XLEN
  const v2 = ((p1) & 0x1n);
  // the answer is uint64_t, 64 bits
  return v1;
}

module.exports = { au_290_c_div_u64_bool };
