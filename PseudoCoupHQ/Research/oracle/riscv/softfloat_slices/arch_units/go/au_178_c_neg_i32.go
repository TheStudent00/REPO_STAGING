// arch-unit 178  --  c  `-a`  lhs=int32_t rhs=None
// symbol op_12   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   subw a0, zero, a0                    integer    operator:- then sign-extend the low 32 bits
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_178_c_neg_i32(p0 uint64) uint64 {
	// a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
	var v1 uint64 = au_sext32(p0); _ = v1
	var v2 uint64 = au_subw(uint64(0x0), v1); _ = v2
	// the answer is int32_t, 32 bits
	return ((v2) & uint64(0xffffffff))
}
