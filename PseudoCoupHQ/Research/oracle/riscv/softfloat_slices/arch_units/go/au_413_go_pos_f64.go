// arch-unit 413  --  go  `+a`  lhs=float64 rhs=None
// symbol main.op_4   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: float64, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_413_go_pos_f64(p0 uint64) uint64 {
	// fa0: operand `a` (float64) arrives in fa0 as a bit pattern
	var v1 uint64 = p0; _ = v1
	// the answer is float64, 64 bits
	return v1
}
