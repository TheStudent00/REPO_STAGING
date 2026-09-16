// arch-unit 69  --  c  `a * b`  lhs=bool rhs=double
// symbol op_208   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
//   fmul.d fa0, fa0, fa5, dyn          float    emulation:f64_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_069_c_mul_bool_f64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended
	var v1 uint64 = ((p0) & uint64(0x1))
	// fa0: operand `b` (double) arrives in fa0
	var v2 uint64 = p1
	var v3 uint64 = emul.Emu_ui32_to_f64_rm0(uint32(v1))
	var v4 uint64 = emul.Emu_f64_mul_rm0(v2, v3)
	return v4
}
