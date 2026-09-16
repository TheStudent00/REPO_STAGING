// arch-unit 50  --  c  `a * b`  lhs=int32_t rhs=float
// symbol op_177   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.w fa5, a0, dyn              float    emulation:i32_to_f32_rm0
//   fmul.s fa0, fa0, fa5, dyn          float    emulation:f32_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_050_c_mul_i32_f32(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int32_t) sign-extended to XLEN
	var v1 uint64 = uint64(int64(int32(uint32(p0))))
	// fa0: operand `b` (float) arrives in fa0
	var v2 uint64 = ((p1) & uint64(0xffffffff))
	var v3 uint64 = emul.Emu_i32_to_f32_rm0(uint32(v1))
	var v4 uint64 = emul.Emu_f32_mul_rm0(v2, v3)
	return ((v4) & uint64(0xffffffff))
}
