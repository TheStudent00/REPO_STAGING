// arch-unit 197  --  c  `sizeof a`  lhs=int32_t rhs=None
// symbol op_48   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x4                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_197_c_sizeof_i32(p0 uint64) uint64 {
	// a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
	var v1 uint64 = au_sext32(p0); _ = v1
	var v2 uint64 = uint64(0x4); _ = v2
	// the answer is uint64_t, 64 bits
	return v2
}
