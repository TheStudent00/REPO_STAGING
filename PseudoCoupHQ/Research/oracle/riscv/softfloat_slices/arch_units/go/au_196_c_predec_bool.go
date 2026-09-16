// arch-unit 196  --  c  `--a`  lhs=bool rhs=None
// symbol op_47   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori a0, a0, 0x1                     integer    operator:^
//   c.jr ra                              integer    return
//
// answer: _Bool, 1 bits.  parameters are operand bit patterns.
package archunits

func Au_196_c_predec_bool(p0 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	var v2 uint64 = au_xor(v1, uint64(0x1)); _ = v2
	// the answer is _Bool, 1 bits
	return ((v2) & uint64(0x1))
}
