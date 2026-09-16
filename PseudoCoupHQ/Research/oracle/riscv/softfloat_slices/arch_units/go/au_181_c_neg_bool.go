// arch-unit 181  --  c  `-a`  lhs=bool rhs=None
// symbol op_17   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_181_c_neg_bool(p0 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	var v2 uint64 = au_sub(uint64(0x0), v1); _ = v2
	// the answer is int32_t, 32 bits
	return ((v2) & uint64(0xffffffff))
}
