// arch-unit 267  --  c  `a - b`  lhs=bool rhs=int32_t
// symbol op_168   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.subw a0, a1                        integer    operator:- then sign-extend the low 32 bits
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_267_c_sub_bool_i32(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	// a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
	var v2 uint64 = au_sext32(p1); _ = v2
	var v3 uint64 = au_subw(v1, v2); _ = v3
	// the answer is int32_t, 32 bits
	return ((v3) & uint64(0xffffffff))
}
