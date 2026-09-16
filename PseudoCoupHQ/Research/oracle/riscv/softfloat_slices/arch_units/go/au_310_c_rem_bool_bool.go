// arch-unit 310  --  c  `a % b`  lhs=bool rhs=bool
// symbol op_281   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x0                         integer    constant
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_310_c_rem_bool_bool(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	// a1: operand `b` (bool) zero-extended to XLEN
	var v2 uint64 = ((p1) & uint64(0x1)); _ = v2
	var v3 uint64 = uint64(0x0); _ = v3
	// the answer is int32_t, 32 bits
	return ((v3) & uint64(0xffffffff))
}
