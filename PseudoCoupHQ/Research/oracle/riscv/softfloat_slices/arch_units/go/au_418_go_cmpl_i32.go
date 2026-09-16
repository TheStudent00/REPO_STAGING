// arch-unit 418  --  go  `^a`  lhs=int32 rhs=None
// symbol main.op_18   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori a0, a0, -0x1                    integer    operator:^
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_418_go_cmpl_i32(p0 uint64) uint64 {
	// a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
	var v1 uint64 = au_sext32(p0); _ = v1
	var v2 uint64 = au_xor(v1, uint64(0xffffffffffffffff)); _ = v2
	// the answer is int32, 32 bits
	return ((v2) & uint64(0xffffffff))
}
