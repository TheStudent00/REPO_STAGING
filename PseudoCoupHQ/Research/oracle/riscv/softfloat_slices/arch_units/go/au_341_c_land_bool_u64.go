// arch-unit 341  --  c  `a && b`  lhs=bool rhs=uint64_t
// symbol op_350   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a1, zero, a1                    integer    operator:< unsigned
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_341_c_land_bool_u64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended to XLEN
	var v1 uint64 = ((p0) & uint64(0x1)); _ = v1
	// a1: operand `b` (uint64_t) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_sltu(uint64(0x0), v2); _ = v3
	var v4 uint64 = au_and(v1, v3); _ = v4
	// the answer is int32_t, 32 bits
	return ((v4) & uint64(0xffffffff))
}
