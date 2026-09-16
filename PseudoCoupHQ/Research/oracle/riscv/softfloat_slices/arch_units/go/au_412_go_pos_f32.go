// arch-unit 412  --  go  `+a`  lhs=float32 rhs=None
// symbol main.op_3   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: float32, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_412_go_pos_f32(p0 uint64) uint64 {
	// fa0: operand `a` (float32) arrives in fa0 as a bit pattern
	var v1 uint64 = ((p0) & uint64(0xffffffff)); _ = v1
	// the answer is float32, 32 bits
	return ((v1) & uint64(0xffffffff))
}
