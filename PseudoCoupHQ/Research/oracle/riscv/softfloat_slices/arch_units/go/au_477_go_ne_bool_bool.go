// arch-unit 477  --  go  `a != b`  lhs=bool rhs=bool
// symbol main.op_527   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub t0, a0, a1                       integer    operator:-
//   sltu a0, zero, t0                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
package archunits

func Au_477_go_ne_bool_bool(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	// a1: operand `b` (bool) zero-extended to XLEN
	var v2 uint64 = ((p1) & uint64(0x1)); _ = v2
	var v3 uint64 = au_sub(v1, v2); _ = v3
	var v4 uint64 = au_sltu(uint64(0x0), v3); _ = v4
	// the answer is bool, 1 bits
	return ((v4) & uint64(0x1))
}
