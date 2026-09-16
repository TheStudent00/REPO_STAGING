// arch-unit 192  --  c  `++a`  lhs=bool rhs=None
// symbol op_41   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x1                         integer    constant
//   c.jr ra                              integer    return
//
// answer: _Bool, 1 bits.  parameters are operand bit patterns.
package archunits

func Au_192_c_preinc_bool(p0 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	var v2 uint64 = uint64(0x1); _ = v2
	// the answer is _Bool, 1 bits
	return ((v2) & uint64(0x1))
}
