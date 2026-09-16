// arch-unit 308  --  c  `a % b`  lhs=bool rhs=int64_t
// symbol op_277   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   rem a0, a0, a1                       integer    written-out restoring division (NOT the language's %)
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_308_c_rem_bool_i64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	// a1: operand `b` (int64_t) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_rem(v1, v2); _ = v3
	// the answer is int64_t, 64 bits
	return v3
}
