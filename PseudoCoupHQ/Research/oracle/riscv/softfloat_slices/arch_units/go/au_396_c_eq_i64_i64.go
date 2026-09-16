// arch-unit 396  --  c  `a == b`  lhs=int64_t rhs=int64_t
// symbol op_469   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_396_c_eq_i64_i64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (int64_t) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_xor(v1, v2); _ = v3
	var v4 uint64 = au_sltu(v3, uint64(0x1)); _ = v4
	// the answer is int32_t, 32 bits
	return ((v4) & uint64(0xffffffff))
}
