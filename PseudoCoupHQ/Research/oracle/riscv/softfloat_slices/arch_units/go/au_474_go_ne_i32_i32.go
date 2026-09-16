// arch-unit 474  --  go  `a != b`  lhs=int32 rhs=int32
// symbol main.op_492   outcome LIFTED   5 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   addiw t0, a0, 0x0                    integer    operator:+ then sign-extend the low 32 bits
//   addiw t1, a1, 0x0                    integer    operator:+ then sign-extend the low 32 bits
//   sub t0, t0, t1                       integer    operator:-
//   sltu a0, zero, t0                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
package archunits

func Au_474_go_ne_i32_i32(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
	var v1 uint64 = au_sext32(p0); _ = v1
	// a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
	var v2 uint64 = au_sext32(p1); _ = v2
	var v3 uint64 = au_addw(v1, uint64(0x0)); _ = v3
	var v4 uint64 = au_addw(v2, uint64(0x0)); _ = v4
	var v5 uint64 = au_sub(v3, v4); _ = v5
	var v6 uint64 = au_sltu(uint64(0x0), v5); _ = v6
	// the answer is bool, 1 bits
	return ((v6) & uint64(0x1))
}
