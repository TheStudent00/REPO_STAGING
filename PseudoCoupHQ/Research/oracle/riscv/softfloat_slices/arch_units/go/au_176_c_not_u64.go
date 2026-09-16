// arch-unit 176  --  c  `!a`  lhs=uint64_t rhs=None
// symbol op_2   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_176_c_not_u64(p0 uint64) uint64 {
	// a0: operand `a` (uint64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	var v2 uint64 = au_sltu(v1, uint64(0x1)); _ = v2
	// the answer is int32_t, 32 bits
	return ((v2) & uint64(0xffffffff))
}
