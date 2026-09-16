// arch-unit 417  --  go  `!a`  lhs=bool rhs=None
// symbol main.op_17   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
package archunits

func Au_417_go_not_bool(p0 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	var v2 uint64 = au_sltu(v1, uint64(0x1)); _ = v2
	// the answer is bool, 1 bits
	return ((v2) & uint64(0x1))
}
