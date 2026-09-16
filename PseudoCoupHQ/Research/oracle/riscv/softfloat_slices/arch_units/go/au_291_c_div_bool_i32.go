// arch-unit 291  --  c  `a / b`  lhs=bool rhs=int32_t
// symbol op_240   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   divw a0, a0, a1                      integer    written-out restoring division (NOT the language's /)
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_291_c_div_bool_i32(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	// a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
	var v2 uint64 = au_sext32(p1); _ = v2
	var v3 uint64 = au_divw(v1, v2); _ = v3
	// the answer is int32_t, 32 bits
	return ((v3) & uint64(0xffffffff))
}
