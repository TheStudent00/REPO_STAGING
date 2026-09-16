// arch-unit 363  --  c  `a ^ b`  lhs=int64_t rhs=int32_t
// symbol op_396   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_363_c_bxor_i64_i32(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
	var v2 uint64 = au_sext32(p1); _ = v2
	var v3 uint64 = au_xor(v1, v2); _ = v3
	// the answer is int64_t, 64 bits
	return v3
}
