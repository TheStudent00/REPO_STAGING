// arch-unit 420  --  go  `^a`  lhs=uint64 rhs=None
// symbol main.op_20   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori a0, a0, -0x1                    integer    operator:^
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_420_go_cmpl_u64(p0 uint64) uint64 {
	// a0: operand `a` (uint64) arrives in a0
	var v1 uint64 = p0; _ = v1
	var v2 uint64 = au_xor(v1, uint64(0xffffffffffffffff)); _ = v2
	// the answer is uint64, 64 bits
	return v2
}
