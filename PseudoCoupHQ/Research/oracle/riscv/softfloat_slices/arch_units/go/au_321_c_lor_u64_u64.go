// arch-unit 321  --  c  `a || b`  lhs=uint64_t rhs=uint64_t
// symbol op_296   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   sltu a0, zero, a0                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_321_c_lor_u64_u64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (uint64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (uint64_t) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_or(v1, v2); _ = v3
	var v4 uint64 = au_sltu(uint64(0x0), v3); _ = v4
	// the answer is int32_t, 32 bits
	return ((v4) & uint64(0xffffffff))
}
