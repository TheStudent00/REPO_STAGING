// arch-unit 286  --  c  `a / b`  lhs=int64_t rhs=bool
// symbol op_221   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_286_c_div_i64_bool(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (bool) zero-extended to XLEN
	var v2 uint64 = ((p1) & uint64(0x1)); _ = v2
	// the answer is int64_t, 64 bits
	return v1
}
