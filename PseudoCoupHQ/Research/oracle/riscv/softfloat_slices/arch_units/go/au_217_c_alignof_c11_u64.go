// arch-unit 217  --  c  `_Alignof a`  lhs=uint64_t rhs=None
// symbol op_80   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x8                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_217_c_alignof_c11_u64(p0 uint64) uint64 {
	// a0: operand `a` (uint64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	var v2 uint64 = uint64(0x8); _ = v2
	// the answer is uint64_t, 64 bits
	return v2
}
