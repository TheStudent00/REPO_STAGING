// arch-unit 455  --  go  `a &^ b`  lhs=int32 rhs=int32
// symbol main.op_276   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori t6, a1, -0x1                    integer    operator:^
//   and a0, a0, t6                       integer    operator:&
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_455_go_andnot_i32_i32(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
	var v1 uint64 = au_sext32(p0); _ = v1
	// a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
	var v2 uint64 = au_sext32(p1); _ = v2
	var v3 uint64 = au_xor(v2, uint64(0xffffffffffffffff)); _ = v3
	var v4 uint64 = au_and(v1, v3); _ = v4
	// the answer is int32, 32 bits
	return ((v4) & uint64(0xffffffff))
}
