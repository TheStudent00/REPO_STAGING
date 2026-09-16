// arch-unit 290  --  c  `a / b`  lhs=uint64_t rhs=bool
// symbol op_227   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_290_c_div_u64_bool(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (uint64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (bool) zero-extended to XLEN
	var v2 uint64 = ((p1) & uint64(0x1)); _ = v2
	// the answer is uint64_t, 64 bits
	return v1
}
