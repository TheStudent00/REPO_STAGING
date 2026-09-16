// arch-unit 349  --  c  `a | b`  lhs=int64_t rhs=uint64_t
// symbol op_362   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_349_c_bor_i64_u64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (uint64_t) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_or(v1, v2); _ = v3
	// the answer is uint64_t, 64 bits
	return v3
}
