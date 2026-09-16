// arch-unit 445  --  go  `a >> b`  lhs=int32 rhs=uint64
// symbol main.op_206   outcome LIFTED   5 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltiu t0, a1, 0x20                   integer    operator:< unsigned
//   c.addi t0, -0x1                      integer    operator:+
//   or t0, a1, t0                        integer    operator:|
//   sraw a0, a0, t0                      integer    arithmetic right shift of the low 32 bits, written out
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_445_go_shr_i32_u64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
	var v1 uint64 = au_sext32(p0); _ = v1
	// a1: operand `b` (uint64) arrives in a1
	var v2 uint64 = p1; _ = v2
	var v3 uint64 = au_sltu(v2, uint64(0x20)); _ = v3
	var v4 uint64 = au_add(v3, uint64(0xffffffffffffffff)); _ = v4
	var v5 uint64 = au_or(v2, v4); _ = v5
	var v6 uint64 = au_sraw(v1, v5); _ = v6
	// the answer is int32, 32 bits
	return ((v6) & uint64(0xffffffff))
}
