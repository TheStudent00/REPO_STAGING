// arch-unit 449  --  go  `a >> b`  lhs=uint64 rhs=int32
// symbol main.op_216   outcome LIFTED   24 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   ld t1, 0x10(s11)                     prologue   stack-growth check -> elided
//   bltu t1, sp, 0x6c738 <main.op_216+0x18> prologue   stack-growth check -> elided
//   c.sdsp a0, 0x8(sp)                   prologue   frame bookkeeping -> elided
//   c.swsp a1, 0x10(sp)                  prologue   stack-growth spill -> elided
//   jal t0, 0x6a790 <runtime.morestack_noctxt.abi0> prologue   stack-growth call / restart / panic tail -> elided
//   c.ldsp a0, 0x8(sp)                   prologue   frame bookkeeping -> elided
//   c.lwsp a1, 0x10(sp)                  prologue   stack-growth reload -> elided
//   jal zero, 0x6c720 <main.op_216>      prologue   stack-growth call / restart / panic tail -> elided
//   sd ra, -0x8(sp)                      frame      frame bookkeeping -> elided
//   c.addi sp, -0x8                      frame      frame bookkeeping -> elided
//   c.sdsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
//   addiw t0, a1, 0x0                    integer    operator:+ then sign-extend the low 32 bits
//   blt t0, zero, 0x6c768 <main.op_216+0x48> guard      guard branch -> a `_trap` predicate
//   srl t0, a0, a1                       integer    operator:>> unsigned (count masked to 6 bits)
//   slli t1, a1, 0x20                    integer    operator:<<
//   srli t1, t1, 0x20                    integer    operator:>> unsigned
//   sltiu t1, t1, 0x40                   integer    operator:< unsigned
//   sub t1, zero, t1                     integer    operator:-
//   and a0, t0, t1                       integer    operator:&
//   c.ldsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
//   c.addi sp, 0x8                       frame      frame bookkeeping -> elided
//   jalr zero, 0x0(ra)                   integer    return
//   jal ra, 0x40830 <runtime.panicshift> trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
//   c.nop                                trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
//
// GUARDED: this arch-unit branches to a go runtime panic.  The function
// below is the fall-through; the companion `_trap` predicate is 1 exactly
// when the arch-unit takes the branch instead.
'use strict';
const AU = require('./au_int.js');

function au_449_go_shr_u64_i32(p0, p1) {
  // a0: operand `a` (uint64) arrives in a0
  const v1 = p0;
  // a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
  const v2 = AU.au_sext32(p1);
  const v3 = AU.au_addw(v2, 0x0n);
  const v4 = AU.au_srl(v1, v2);
  const v5 = AU.au_sll(v2, 0x20n);
  const v6 = AU.au_srl(v5, 0x20n);
  const v7 = AU.au_sltu(v6, 0x40n);
  const v8 = AU.au_sub(0x0n, v7);
  const v9 = AU.au_and(v4, v8);
  // the answer is uint64, 64 bits
  return v9;
}

function au_449_go_shr_u64_i32_trap(p0, p1) {
  // a0: operand `a` (uint64) arrives in a0
  const v1 = p0;
  // a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
  const v2 = AU.au_sext32(p1);
  const v3 = AU.au_addw(v2, 0x0n);
  return AU.au_ltz(v3);
}

module.exports = { au_449_go_shr_u64_i32, au_449_go_shr_u64_i32_trap };
