// arch-unit 415  --  go  `-a`  lhs=int64 rhs=None
// symbol main.op_7   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_415_go_neg_i64(p0 uint64) uint64 {
	// a0: operand `a` (int64) arrives in a0
	var v1 uint64 = p0; _ = v1
	var v2 uint64 = au_sub(uint64(0x0), v1); _ = v2
	// the answer is int64, 64 bits
	return v2
}
