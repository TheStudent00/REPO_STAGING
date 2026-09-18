// arch-unit 417  --  go  `!a`  lhs=bool rhs=None
// symbol main.op_17   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_417_go_not_bool(p0) {
  // a0: operand `a` (bool) zero-extended to XLEN
  const v1 = ((p0) & 0x1n);
  const v2 = AU.au_sltu(v1, 0x1n);
  // the answer is bool, 1 bits
  return ((v2) & 0x1n);
}

module.exports = { au_417_go_not_bool };
