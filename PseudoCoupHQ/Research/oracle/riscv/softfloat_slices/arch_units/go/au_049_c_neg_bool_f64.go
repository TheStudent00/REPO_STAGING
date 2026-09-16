// arch-unit 49  --  c  `a - b`  lhs=bool rhs=double
// symbol op_172   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
//   fsub.d fa0, fa5, fa0, dyn          float    emulation:f64_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_049_c_neg_bool_f64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended
	var v1 uint64 = ((p0) & uint64(0x1))
	// fa0: operand `b` (double) arrives in fa0
	var v2 uint64 = p1
	var v3 uint64 = emul.Emu_ui32_to_f64_rm0(uint32(v1))
	var v4 uint64 = emul.Emu_f64_sub_rm0(v3, v2)
	return v4
}
