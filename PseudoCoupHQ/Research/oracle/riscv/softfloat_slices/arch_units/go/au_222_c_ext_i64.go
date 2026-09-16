// arch-unit 222  --  c  `__extension__ a`  lhs=int64_t rhs=None
// symbol op_85   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_222_c_ext_i64(p0 uint64) uint64 {
	// a0: operand `a` (int64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	// the answer is int64_t, 64 bits
	return v1
}
