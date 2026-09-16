// arch-unit 426  --  go  `a * b`  lhs=int64 rhs=int64
// symbol main.op_67   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   mul a0, a0, a1                       integer    operator:*
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_426_go_mul_i64_i64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int64) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (int64) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_mul(v1, v2); _ = v3
	// the answer is int64, 64 bits
	return v3
}
