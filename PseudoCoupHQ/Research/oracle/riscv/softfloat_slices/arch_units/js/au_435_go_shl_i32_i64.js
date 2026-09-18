// arch-unit 435  --  go  `a << b`  lhs=int32 rhs=int64
// symbol main.op_169   outcome LIFTED   21 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   ld t1, 0x10(s11)                     prologue   stack-growth check -> elided
//   bltu t1, sp, 0x6c748 <main.op_169+0x18> prologue   stack-growth check -> elided
//   c.swsp a0, 0x8(sp)                   prologue   stack-growth spill -> elided
//   c.sdsp a1, 0x10(sp)                  prologue   frame bookkeeping -> elided
//   jal t0, 0x6a7a0 <runtime.morestack_noctxt.abi0> prologue   stack-growth call / restart / panic tail -> elided
//   c.lwsp a0, 0x8(sp)                   prologue   stack-growth reload -> elided
//   c.ldsp a1, 0x10(sp)                  prologue   frame bookkeeping -> elided
//   jal zero, 0x6c730 <main.op_169>      prologue   stack-growth call / restart / panic tail -> elided
//   sd ra, -0x8(sp)                      frame      frame bookkeeping -> elided
//   c.addi sp, -0x8                      frame      frame bookkeeping -> elided
//   c.sdsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
//   blt a1, zero, 0x6c76c <main.op_169+0x3c> guard      guard branch -> a `_trap` predicate
//   sll t0, a0, a1                       integer    operator:<< (count masked to 6 bits)
//   sltiu t1, a1, 0x40                   integer    operator:< unsigned
//   sub t1, zero, t1                     integer    operator:-
//   and a0, t0, t1                       integer    operator:&
//   c.ldsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
//   c.addi sp, 0x8                       frame      frame bookkeeping -> elided
//   jalr zero, 0x0(ra)                   integer    return
//   jal ra, 0x408a0 <runtime.panicshift> trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
//   c.nop                                trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
//
// GUARDED: this arch-unit branches to a go runtime panic.  The function
// below is the fall-through; the companion `_trap` predicate is 1 exactly
// when the arch-unit takes the branch instead.
'use strict';
const AU = require('./au_int.js');

function au_435_go_shl_i32_i64(p0, p1) {
  // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
  const v1 = AU.au_sext32(p0);
  // a1: operand `b` (int64) arrives in a1
  const v2 = p1;
  const v3 = AU.au_sll(v1, v2);
  const v4 = AU.au_sltu(v2, 0x40n);
  const v5 = AU.au_sub(0x0n, v4);
  const v6 = AU.au_and(v3, v5);
  // the answer is int32, 32 bits
  return ((v6) & 0xffffffffn);
}

function au_435_go_shl_i32_i64_trap(p0, p1) {
  // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
  const v1 = AU.au_sext32(p0);
  // a1: operand `b` (int64) arrives in a1
  const v2 = p1;
  return AU.au_ltz(v2);
}

module.exports = { au_435_go_shl_i32_i64, au_435_go_shl_i32_i64_trap };
