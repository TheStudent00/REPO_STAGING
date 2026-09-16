// arch-unit 466  --  go  `a | b`  lhs=uint64 rhs=uint64
// symbol main.op_398   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_466_go_bor_u64_u64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (uint64) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (uint64) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_or(v1, v2); _ = v3
	// the answer is uint64, 64 bits
	return v3
}
