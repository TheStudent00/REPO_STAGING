// arch-unit 254  --  c  `a + b`  lhs=bool rhs=bool
// symbol op_137   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.add a0, a1                         integer    operator:+
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_254_c_add_bool_bool(p0, p1) {
  // a0: operand `a` (bool) zero-extended to XLEN
  const v1 = ((p0) & 0x1n);
  // a1: operand `b` (bool) zero-extended to XLEN
  const v2 = ((p1) & 0x1n);
  const v3 = AU.au_add(v1, v2);
  // the answer is int32_t, 32 bits
  return ((v3) & 0xffffffffn);
}

module.exports = { au_254_c_add_bool_bool };
