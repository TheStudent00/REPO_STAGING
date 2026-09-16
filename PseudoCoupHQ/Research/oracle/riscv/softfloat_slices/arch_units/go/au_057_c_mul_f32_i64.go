// arch-unit 57  --  c  `a * b`  lhs=float rhs=int64_t
// symbol op_193   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.l fa5, a0, dyn              float    emulation:i64_to_f32_rm0
//   fmul.s fa0, fa0, fa5, dyn          float    emulation:f32_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_057_c_mul_f32_i64(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float) arrives in fa0
	var v1 uint64 = ((p0) & uint64(0xffffffff))
	// a0: operand `b` (int64_t) arrives in a0
	var v2 uint64 = p1
	var v3 uint64 = emul.Emu_i64_to_f32_rm0(v2)
	var v4 uint64 = emul.Emu_f32_mul_rm0(v1, v3)
	return ((v4) & uint64(0xffffffff))
}
