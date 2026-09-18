// arch-unit 337  --  c  `a && b`  lhs=uint64_t rhs=uint64_t
// symbol op_332   outcome LIFTED   4 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                    integer    operator:< unsigned
//   sltu a1, zero, a1                    integer    operator:< unsigned
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_337_c_land_u64_u64(p0, p1) {
  // a0: operand `a` (uint64_t) arrives in a0
  const v1 = p0;
  // a1: operand `b` (uint64_t) arrives in a1
  const v2 = p1;
  const v3 = AU.au_sltu(0x0n, v1);
  const v4 = AU.au_sltu(0x0n, v2);
  const v5 = AU.au_and(v3, v4);
  // the answer is int32_t, 32 bits
  return ((v5) & 0xffffffffn);
}

module.exports = { au_337_c_land_u64_u64 };
