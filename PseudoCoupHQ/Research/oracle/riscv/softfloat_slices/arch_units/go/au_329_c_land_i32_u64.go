// arch-unit 329  --  c  `a && b`  lhs=int32_t rhs=uint64_t
// symbol op_320   outcome LIFTED   4 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                    integer    operator:< unsigned
//   sltu a1, zero, a1                    integer    operator:< unsigned
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_329_c_land_i32_u64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
	var v1 uint64 = au_sext32(p0); _ = v1
	// a1: operand `b` (uint64_t) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_sltu(uint64(0x0), v1); _ = v3
	var v4 uint64 = au_sltu(uint64(0x0), v2); _ = v4
	var v5 uint64 = au_and(v3, v4); _ = v5
	// the answer is int32_t, 32 bits
	return ((v5) & uint64(0xffffffff))
}
