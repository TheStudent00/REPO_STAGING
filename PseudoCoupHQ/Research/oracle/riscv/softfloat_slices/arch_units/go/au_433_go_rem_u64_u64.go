// arch-unit 433  --  go  `a % b`  lhs=uint64 rhs=uint64
// symbol main.op_146   outcome LIFTED   18 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   ld t1, 0x10(s11)                     prologue   stack-growth check -> elided
//   bltu t1, sp, 0x6c738 <main.op_146+0x18> prologue   stack-growth check -> elided
//   c.sdsp a0, 0x8(sp)                   prologue   frame bookkeeping -> elided
//   c.sdsp a1, 0x10(sp)                  prologue   frame bookkeeping -> elided
//   jal t0, 0x6a790 <runtime.morestack_noctxt.abi0> prologue   stack-growth call / restart / panic tail -> elided
//   c.ldsp a0, 0x8(sp)                   prologue   frame bookkeeping -> elided
//   c.ldsp a1, 0x10(sp)                  prologue   frame bookkeeping -> elided
//   jal zero, 0x6c720 <main.op_146>      prologue   stack-growth call / restart / panic tail -> elided
//   sd ra, -0x8(sp)                      frame      frame bookkeeping -> elided
//   c.addi sp, -0x8                      frame      frame bookkeeping -> elided
//   c.sdsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
//   beq a1, zero, 0x6c750 <main.op_146+0x30> guard      guard branch -> a `_trap` predicate
//   remu a0, a0, a1                      integer    written-out restoring division (NOT the language's %)
//   c.ldsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
//   c.addi sp, 0x8                       frame      frame bookkeeping -> elided
//   jalr zero, 0x0(ra)                   integer    return
//   jal ra, 0x40878 <runtime.panicdivide> trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
//   c.nop                                trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
//
// GUARDED: this arch-unit branches to a go runtime panic.  The function
// below is the fall-through; the companion `_trap` predicate is 1 exactly
// when the arch-unit takes the branch instead.
package archunits

func Au_433_go_rem_u64_u64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (uint64) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (uint64) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_remu(v1, v2); _ = v3
	// the answer is uint64, 64 bits
	return v3
}

func Au_433_go_rem_u64_u64_trap(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (uint64) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (uint64) arrives in a1
	var v2 uint64 = p1; _ = v2
	return au_eqz(v2)
}
