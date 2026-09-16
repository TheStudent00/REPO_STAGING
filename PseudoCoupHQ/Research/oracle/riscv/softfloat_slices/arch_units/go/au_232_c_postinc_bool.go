// arch-unit 232  --  c  `a++`  lhs=bool rhs=None
// symbol op_95   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: _Bool, 1 bits.  parameters are operand bit patterns.
package archunits

func Au_232_c_postinc_bool(p0 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	// the answer is _Bool, 1 bits
	return ((v1) & uint64(0x1))
}
