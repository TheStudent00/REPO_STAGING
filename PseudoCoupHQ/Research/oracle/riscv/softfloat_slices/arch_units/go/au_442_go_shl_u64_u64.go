// arch-unit 442  --  go  `a << b`  lhs=uint64 rhs=uint64
// symbol main.op_182   outcome LIFTED   5 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sll t0, a0, a1                       integer    operator:<< (count masked to 6 bits)
//   sltiu t1, a1, 0x40                   integer    operator:< unsigned
//   sub t1, zero, t1                     integer    operator:-
//   and a0, t0, t1                       integer    operator:&
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_442_go_shl_u64_u64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (uint64) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (uint64) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_sll(v1, v2); _ = v3
	var v4 uint64 = au_sltu(v2, uint64(0x40)); _ = v4
	var v5 uint64 = au_sub(uint64(0x0), v4); _ = v5
	var v6 uint64 = au_and(v3, v5); _ = v6
	// the answer is uint64, 64 bits
	return v6
}
