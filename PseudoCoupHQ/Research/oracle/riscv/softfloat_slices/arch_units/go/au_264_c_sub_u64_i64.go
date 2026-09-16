// arch-unit 264  --  c  `a - b`  lhs=uint64_t rhs=int64_t
// symbol op_151   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.sub a0, a1                         integer    operator:-
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_264_c_sub_u64_i64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (uint64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (int64_t) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_sub(v1, v2); _ = v3
	// the answer is uint64_t, 64 bits
	return v3
}
