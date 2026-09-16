// arch-unit 237  --  c  `a--`  lhs=double rhs=None
// symbol op_100   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: double, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_237_c_postdec_f64(p0 uint64) uint64 {
	// fa0: operand `a` (double) arrives in fa0 as a bit pattern
	var v1 uint64 = p0; _ = v1
	// the answer is double, 64 bits
	return v1
}
