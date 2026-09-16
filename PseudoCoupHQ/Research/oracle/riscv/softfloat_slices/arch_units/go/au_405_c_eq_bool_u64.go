// arch-unit 405  --  c  `a == b`  lhs=bool rhs=uint64_t
// symbol op_494   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_405_c_eq_bool_u64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	// a1: operand `b` (uint64_t) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_xor(v1, v2); _ = v3
	var v4 uint64 = au_sltu(v3, uint64(0x1)); _ = v4
	// the answer is int32_t, 32 bits
	return ((v4) & uint64(0xffffffff))
}
