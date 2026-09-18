// arch-unit 190  --  c  `++a`  lhs=int64_t rhs=None
// symbol op_37   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.addi a0, 0x1                       integer    operator:+
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_190_c_preinc_i64(p0) {
  // a0: operand `a` (int64_t) arrives in a0
  const v1 = p0;
  const v2 = AU.au_add(v1, 0x1n);
  // the answer is int64_t, 64 bits
  return v2;
}

module.exports = { au_190_c_preinc_i64 };
