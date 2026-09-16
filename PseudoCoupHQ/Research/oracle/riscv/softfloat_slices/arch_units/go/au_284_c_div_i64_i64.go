// arch-unit 284  --  c  `a / b`  lhs=int64_t rhs=int64_t
// symbol op_217   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   div a0, a0, a1                       integer    written-out restoring division (NOT the language's /)
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_284_c_div_i64_i64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (int64_t) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_div(v1, v2); _ = v3
	// the answer is int64_t, 64 bits
	return v3
}
