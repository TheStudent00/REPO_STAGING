// arch-unit 273  --  c  `a * b`  lhs=int64_t rhs=bool
// symbol op_185   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   czero.eqz a0, a0, a1                 integer    conditional select
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_273_c_mul_i64_bool(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (bool) zero-extended to XLEN
	var v2 uint64 = ((p1) & uint64(0x1)); _ = v2
	var v3 uint64 = au_czeqz(v1, v2); _ = v3
	// the answer is int64_t, 64 bits
	return v3
}
