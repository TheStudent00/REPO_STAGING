// arch-unit 84  --  c  `a / b`  lhs=double rhs=uint64_t
// symbol op_236   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.lu fa5, a0, dyn             float    emulation:ui64_to_f64_rm0
//   fdiv.d fa0, fa0, fa5, dyn          float    emulation:f64_div_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_084_c_div_f64_u64(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (double) arrives in fa0
	var v1 uint64 = p0
	// a0: operand `b` (uint64_t) arrives in a0
	var v2 uint64 = p1
	var v3 uint64 = emul.Emu_ui64_to_f64_rm0(v2)
	var v4 uint64 = emul.Emu_f64_div_rm0(v1, v3)
	return v4
}
