// arch-unit 233  --  c  `a--`  lhs=int32_t rhs=None
// symbol op_96   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_233_c_postdec_i32(p0 uint64) uint64 {
	// a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
	var v1 uint64 = au_sext32(p0); _ = v1
	// the answer is int32_t, 32 bits
	return ((v1) & uint64(0xffffffff))
}
