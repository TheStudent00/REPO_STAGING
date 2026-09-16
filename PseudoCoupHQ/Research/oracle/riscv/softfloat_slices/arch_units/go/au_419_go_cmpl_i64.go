// arch-unit 419  --  go  `^a`  lhs=int64 rhs=None
// symbol main.op_19   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori a0, a0, -0x1                    integer    operator:^
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_419_go_cmpl_i64(p0 uint64) uint64 {
	// a0: operand `a` (int64) arrives in a0
	var v1 uint64 = p0; _ = v1
	var v2 uint64 = au_xor(v1, uint64(0xffffffffffffffff)); _ = v2
	// the answer is int64, 64 bits
	return v2
}
