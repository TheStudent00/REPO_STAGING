// arch-unit 318  --  c  `a || b`  lhs=int64_t rhs=bool
// symbol op_293   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                    integer    operator:< unsigned
//   c.or a0, a1                          integer    operator:|
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_318_c_lor_i64_bool(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (bool) zero-extended to XLEN
	var v2 uint64 = ((p1) & uint64(0x1)); _ = v2
	var v3 uint64 = au_sltu(uint64(0x0), v1); _ = v3
	var v4 uint64 = au_or(v3, v2); _ = v4
	// the answer is int32_t, 32 bits
	return ((v4) & uint64(0xffffffff))
}
