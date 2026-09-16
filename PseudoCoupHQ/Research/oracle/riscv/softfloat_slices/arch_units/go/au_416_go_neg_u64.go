// arch-unit 416  --  go  `-a`  lhs=uint64 rhs=None
// symbol main.op_8   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_416_go_neg_u64(p0 uint64) uint64 {
	// a0: operand `a` (uint64) arrives in a0
	var v1 uint64 = p0; _ = v1
	var v2 uint64 = au_sub(uint64(0x0), v1); _ = v2
	// the answer is uint64, 64 bits
	return v2
}
