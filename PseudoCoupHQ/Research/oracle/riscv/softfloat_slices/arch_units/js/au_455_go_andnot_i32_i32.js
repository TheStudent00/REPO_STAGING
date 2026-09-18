// arch-unit 455  --  go  `a &^ b`  lhs=int32 rhs=int32
// symbol main.op_276   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori t6, a1, -0x1                    integer    operator:^
//   and a0, a0, t6                       integer    operator:&
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_455_go_andnot_i32_i32(p0, p1) {
  // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
  const v1 = AU.au_sext32(p0);
  // a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
  const v2 = AU.au_sext32(p1);
  const v3 = AU.au_xor(v2, 0xffffffffffffffffn);
  const v4 = AU.au_and(v1, v3);
  // the answer is int32, 32 bits
  return ((v4) & 0xffffffffn);
}

module.exports = { au_455_go_andnot_i32_i32 };
