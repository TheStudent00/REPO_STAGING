// arch-unit 266  --  c  `a - b`  lhs=uint64_t rhs=bool
// symbol op_155   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.sub a0, a1                         integer    operator:-
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_266_c_sub_u64_bool(p0, p1) {
  // a0: operand `a` (uint64_t) arrives in a0
  const v1 = p0;
  // a1: operand `b` (bool) zero-extended to XLEN
  const v2 = ((p1) & 0x1n);
  const v3 = AU.au_sub(v1, v2);
  // the answer is uint64_t, 64 bits
  return v3;
}

module.exports = { au_266_c_sub_u64_bool };
