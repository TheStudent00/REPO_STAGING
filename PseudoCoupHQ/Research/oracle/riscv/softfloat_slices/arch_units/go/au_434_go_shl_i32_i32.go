// arch-unit 434  --  go  `a << b`  lhs=int32 rhs=int32
// symbol main.op_168   outcome LIFTED   24 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   ld t1, 0x10(s11)                     prologue   stack-growth check -> elided
//   bltu t1, sp, 0x6c748 <main.op_168+0x18> prologue   stack-growth check -> elided
//   c.swsp a0, 0x8(sp)                   prologue   stack-growth spill -> elided
//   c.swsp a1, 0xc(sp)                   prologue   stack-growth spill -> elided
//   jal t0, 0x6a7a0 <runtime.morestack_noctxt.abi0> prologue   stack-growth call / restart / panic tail -> elided
//   c.lwsp a0, 0x8(sp)                   prologue   stack-growth reload -> elided
//   c.lwsp a1, 0xc(sp)                   prologue   stack-growth reload -> elided
//   jal zero, 0x6c730 <main.op_168>      prologue   stack-growth call / restart / panic tail -> elided
//   sd ra, -0x8(sp)                      frame      frame bookkeeping -> elided
//   c.addi sp, -0x8                      frame      frame bookkeeping -> elided
//   c.sdsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
//   addiw t0, a1, 0x0                    integer    operator:+ then sign-extend the low 32 bits
//   blt t0, zero, 0x6c778 <main.op_168+0x48> guard      guard branch -> a `_trap` predicate
//   sll t0, a0, a1                       integer    operator:<< (count masked to 6 bits)
//   slli t1, a1, 0x20                    integer    operator:<<
//   srli t1, t1, 0x20                    integer    operator:>> unsigned
//   sltiu t1, t1, 0x40                   integer    operator:< unsigned
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
package archunits

func Au_434_go_shl_i32_i32(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
	var v1 uint64 = au_sext32(p0); _ = v1
	// a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
	var v2 uint64 = au_sext32(p1); _ = v2
	var v3 uint64 = au_addw(v2, uint64(0x0)); _ = v3
	var v4 uint64 = au_sll(v1, v2); _ = v4
	var v5 uint64 = au_sll(v2, uint64(0x20)); _ = v5
	var v6 uint64 = au_srl(v5, uint64(0x20)); _ = v6
	var v7 uint64 = au_sltu(v6, uint64(0x40)); _ = v7
	var v8 uint64 = au_sub(uint64(0x0), v7); _ = v8
	var v9 uint64 = au_and(v4, v8); _ = v9
	// the answer is int32, 32 bits
	return ((v9) & uint64(0xffffffff))
}

func Au_434_go_shl_i32_i32_trap(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
	var v1 uint64 = au_sext32(p0); _ = v1
	// a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
	var v2 uint64 = au_sext32(p1); _ = v2
	var v3 uint64 = au_addw(v2, uint64(0x0)); _ = v3
	return au_ltz(v3)
}
