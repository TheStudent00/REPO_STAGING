// arch-unit 20  --  c  `a + b`  lhs=float rhs=double
// symbol op_124   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.s fa5, fa0                  float    emulation:f32_to_f64_rm0
//   fadd.d fa0, fa1, fa5, dyn          float    emulation:f64_add_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_020_c_add_f32_f64(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float) arrives in fa0
	var v1 uint64 = ((p0) & uint64(0xffffffff))
	// fa1: operand `b` (double) arrives in fa1
	var v2 uint64 = p1
	var v3 uint64 = emul.Emu_f32_to_f64_rm0(v1)
	var v4 uint64 = emul.Emu_f64_add_rm0(v2, v3)
	return v4
}
