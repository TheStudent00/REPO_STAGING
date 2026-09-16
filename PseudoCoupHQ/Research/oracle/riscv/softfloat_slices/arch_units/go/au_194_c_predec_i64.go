// arch-unit 194  --  c  `--a`  lhs=int64_t rhs=None
// symbol op_43   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.addi a0, -0x1                      integer    operator:+
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_194_c_predec_i64(p0 uint64) uint64 {
	// a0: operand `a` (int64_t) arrives in a0
	var v1 uint64 = p0; _ = v1
	var v2 uint64 = au_add(v1, uint64(0xffffffffffffffff)); _ = v2
	// the answer is int64_t, 64 bits
	return v2
}
