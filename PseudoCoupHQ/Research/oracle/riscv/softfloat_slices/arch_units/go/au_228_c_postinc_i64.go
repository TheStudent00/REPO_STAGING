// arch-unit 228  --  c  `a++`  lhs=int64_t rhs=None
// symbol op_91   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_228_c_postinc_i64(p0 uint64) uint64 {
	// a0: operand `a` (int64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	// the answer is int64_t, 64 bits
	return v1
}
