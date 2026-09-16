// arch-unit 86  --  c  `a / b`  lhs=double rhs=double
// symbol op_238   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fdiv.d fa0, fa0, fa1, dyn          float    emulation:f64_div_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_086_c_div_f64_f64(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (double) arrives in fa0
	var v1 uint64 = p0
	// fa1: operand `b` (double) arrives in fa1
	var v2 uint64 = p1
	var v3 uint64 = emul.Emu_f64_div_rm0(v1, v2)
	return v3
}
