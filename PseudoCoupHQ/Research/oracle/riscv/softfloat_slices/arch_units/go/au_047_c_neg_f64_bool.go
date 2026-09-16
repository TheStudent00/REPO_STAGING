// arch-unit 47  --  c  `a - b`  lhs=double rhs=bool
// symbol op_167   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
//   fsub.d fa0, fa0, fa5, dyn          float    emulation:f64_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_047_c_neg_f64_bool(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (double) arrives in fa0
	var v1 uint64 = p0
	// a0: operand `b` (bool) zero-extended
	var v2 uint64 = ((p1) & uint64(0x1))
	var v3 uint64 = emul.Emu_ui32_to_f64_rm0(uint32(v2))
	var v4 uint64 = emul.Emu_f64_sub_rm0(v1, v3)
	return v4
}
