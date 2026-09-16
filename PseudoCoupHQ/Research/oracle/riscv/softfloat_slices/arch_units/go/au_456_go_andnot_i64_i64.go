// arch-unit 456  --  go  `a &^ b`  lhs=int64 rhs=int64
// symbol main.op_283   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori t6, a1, -0x1                    integer    operator:^
//   and a0, a0, t6                       integer    operator:&
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_456_go_andnot_i64_i64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int64) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (int64) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_xor(v2, uint64(0xffffffffffffffff)); _ = v3
	var v4 uint64 = au_and(v1, v3); _ = v4
	// the answer is int64, 64 bits
	return v4
}
