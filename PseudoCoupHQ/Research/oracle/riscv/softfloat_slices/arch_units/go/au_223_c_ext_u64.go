// arch-unit 223  --  c  `__extension__ a`  lhs=uint64_t rhs=None
// symbol op_86   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_223_c_ext_u64(p0 uint64) uint64 {
	// a0: operand `a` (uint64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	// the answer is uint64_t, 64 bits
	return v1
}
