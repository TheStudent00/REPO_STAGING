// arch-unit 485  --  go  `a > b`  lhs=int64 rhs=int64
// symbol main.op_607   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   slt a0, a1, a0                       integer    operator:< signed
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
package archunits

func Au_485_go_gt_i64_i64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int64) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (int64) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_slt(v2, v1); _ = v3
	// the answer is bool, 1 bits
	return ((v3) & uint64(0x1))
}
