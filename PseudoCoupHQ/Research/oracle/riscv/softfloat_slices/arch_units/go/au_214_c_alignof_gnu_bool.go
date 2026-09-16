// arch-unit 214  --  c  `__alignof a`  lhs=bool rhs=None
// symbol op_65   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x1                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_214_c_alignof_gnu_bool(p0 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	var v2 uint64 = uint64(0x1); _ = v2
	// the answer is uint64_t, 64 bits
	return v2
}
