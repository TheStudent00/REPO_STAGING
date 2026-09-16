// arch-unit 461  --  go  `a - b`  lhs=int32 rhs=int32
// symbol main.op_348   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.sub a0, a1                         integer    operator:-
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_461_go_sub_i32_i32(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
	var v1 uint64 = au_sext32(p0); _ = v1
	// a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
	var v2 uint64 = au_sext32(p1); _ = v2
	var v3 uint64 = au_sub(v1, v2); _ = v3
	// the answer is int32, 32 bits
	return ((v3) & uint64(0xffffffff))
}
