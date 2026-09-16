// arch-unit 486  --  go  `a > b`  lhs=uint64 rhs=uint64
// symbol main.op_614   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, a1, a0                      integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
package archunits

func Au_486_go_gt_u64_u64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (uint64) arrives in a0
	var v1 uint64 = p0; _ = v1
	// a1: operand `b` (uint64) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_sltu(v2, v1); _ = v3
	// the answer is bool, 1 bits
	return ((v3) & uint64(0x1))
}
