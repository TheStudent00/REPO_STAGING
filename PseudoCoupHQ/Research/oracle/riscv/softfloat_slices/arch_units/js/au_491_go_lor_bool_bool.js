// arch-unit 491  --  go  `a || b`  lhs=bool rhs=bool
// symbol main.op_743   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_491_go_lor_bool_bool(p0, p1) {
  // a0: operand `a` (bool) zero-extended to XLEN
  const v1 = ((p0) & 0x1n);
  // a1: operand `b` (bool) zero-extended to XLEN
  const v2 = ((p1) & 0x1n);
  const v3 = AU.au_or(v1, v2);
  // the answer is bool, 1 bits
  return ((v3) & 0x1n);
}

module.exports = { au_491_go_lor_bool_bool };
