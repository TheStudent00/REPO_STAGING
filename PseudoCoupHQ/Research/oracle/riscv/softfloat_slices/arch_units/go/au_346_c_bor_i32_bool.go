// arch-unit 346  --  c  `a | b`  lhs=int32_t rhs=bool
// symbol op_359   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_346_c_bor_i32_bool(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
	var v1 uint64 = au_sext32(p0); _ = v1
	// a1: operand `b` (bool) zero-extended to XLEN
	var v2 uint64 = ((p1) & uint64(0x1)); _ = v2
	var v3 uint64 = au_or(v1, v2); _ = v3
	// the answer is int32_t, 32 bits
	return ((v3) & uint64(0xffffffff))
}
