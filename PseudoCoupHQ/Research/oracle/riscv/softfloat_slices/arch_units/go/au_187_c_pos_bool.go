// arch-unit 187  --  c  `+a`  lhs=bool rhs=None
// symbol op_23   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_187_c_pos_bool(p0 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	// the answer is int32_t, 32 bits
	return ((v1) & uint64(0xffffffff))
}
