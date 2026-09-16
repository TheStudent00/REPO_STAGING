// arch-unit 65  --  c  `a * b`  lhs=double rhs=float
// symbol op_201   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.s fa5, fa1                  float    emulation:f32_to_f64_rm0
//   fmul.d fa0, fa0, fa5, dyn          float    emulation:f64_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_065_c_mul_f64_f32(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (double) arrives in fa0
	var v1 uint64 = p0
	// fa1: operand `b` (float) arrives in fa1
	var v2 uint64 = ((p1) & uint64(0xffffffff))
	var v3 uint64 = emul.Emu_f32_to_f64_rm0(v2)
	var v4 uint64 = emul.Emu_f64_mul_rm0(v1, v3)
	return v4
}
