// arch-unit 73  --  c  `a / b`  lhs=int64_t rhs=double
// symbol op_220   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.l fa5, a0, dyn              float    emulation:i64_to_f64_rm0
//   fdiv.d fa0, fa5, fa0, dyn          float    emulation:f64_div_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_073_c_div_i64_f64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int64_t) arrives in a0
	var v1 uint64 = p0
	// fa0: operand `b` (double) arrives in fa0
	var v2 uint64 = p1
	var v3 uint64 = emul.Emu_i64_to_f64_rm0(v1)
	var v4 uint64 = emul.Emu_f64_div_rm0(v3, v2)
	return v4
}
