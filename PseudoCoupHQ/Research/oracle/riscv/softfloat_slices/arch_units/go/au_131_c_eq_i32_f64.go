// arch-unit 131  --  c  `a == b`  lhs=int32_t rhs=double
// symbol op_466   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.w fa5, a0                   float    emulation:i32_to_f64_rm0
//   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_131_c_eq_i32_f64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int32_t) sign-extended to XLEN
	var v1 uint64 = uint64(int64(int32(uint32(p0))))
	// fa0: operand `b` (double) arrives in fa0
	var v2 uint64 = p1
	var v3 uint64 = emul.Emu_i32_to_f64_rm0(uint32(v1))
	var v4 uint64 = b2u(emul.Emu_f64_eq_rm0(v2, v3))
	return v4
}
