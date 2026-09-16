// arch-unit 216  --  c  `_Alignof a`  lhs=int64_t rhs=None
// symbol op_79   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x8                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_216_c_alignof_c11_i64(p0 uint64) uint64 {
	// a0: operand `a` (int64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	var v2 uint64 = uint64(0x8); _ = v2
	// the answer is uint64_t, 64 bits
	return v2
}
