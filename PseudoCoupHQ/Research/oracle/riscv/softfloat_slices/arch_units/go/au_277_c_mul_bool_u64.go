// arch-unit 277  --  c  `a * b`  lhs=bool rhs=uint64_t
// symbol op_206   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   czero.eqz a0, a1, a0                 integer    conditional select
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_277_c_mul_bool_u64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	// a1: operand `b` (uint64_t) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_czeqz(v2, v1); _ = v3
	// the answer is uint64_t, 64 bits
	return v3
}
