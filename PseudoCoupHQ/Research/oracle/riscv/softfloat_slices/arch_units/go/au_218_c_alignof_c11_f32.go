// arch-unit 218  --  c  `_Alignof a`  lhs=float rhs=None
// symbol op_81   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x4                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_218_c_alignof_c11_f32(p0 uint64) uint64 {
	// fa0: operand `a` (float) arrives in fa0 as a bit pattern
	var v1 uint64 = ((p0) & uint64(0xffffffff)); _ = v1
	var v2 uint64 = uint64(0x4); _ = v2
	// the answer is uint64_t, 64 bits
	return v2
}
