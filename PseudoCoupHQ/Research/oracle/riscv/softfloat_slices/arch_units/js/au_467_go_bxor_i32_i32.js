// arch-unit 467  --  go  `a ^ b`  lhs=int32 rhs=int32
// symbol main.op_420   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_467_go_bxor_i32_i32(p0, p1) {
  // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
  const v1 = AU.au_sext32(p0);
  // a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
  const v2 = AU.au_sext32(p1);
  const v3 = AU.au_xor(v1, v2);
  // the answer is int32, 32 bits
  return ((v3) & 0xffffffffn);
}

module.exports = { au_467_go_bxor_i32_i32 };
