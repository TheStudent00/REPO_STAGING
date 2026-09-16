// arch-unit 230  --  c  `a++`  lhs=float rhs=None
// symbol op_93   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: float, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_230_c_postinc_f32(p0 uint64) uint64 {
	// fa0: operand `a` (float) arrives in fa0 as a bit pattern
	var v1 uint64 = ((p0) & uint64(0xffffffff)); _ = v1
	// the answer is float, 32 bits
	return ((v1) & uint64(0xffffffff))
}
