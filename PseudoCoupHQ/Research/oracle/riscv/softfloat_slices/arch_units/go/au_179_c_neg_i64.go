// arch-unit 179  --  c  `-a`  lhs=int64_t rhs=None
// symbol op_13   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_179_c_neg_i64(p0 uint64) uint64 {
	// a0: operand `a` (int64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	var v2 uint64 = au_sub(uint64(0x0), v1); _ = v2
	// the answer is int64_t, 64 bits
	return v2
}
