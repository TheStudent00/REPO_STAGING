// arch-unit 41  --  c  `a - b`  lhs=float rhs=bool
// symbol op_161   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.wu fa5, a0, dyn             float    emulation:ui32_to_f32_rm0
//   fsub.s fa0, fa0, fa5, dyn          float    emulation:f32_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_041_c_neg_f32_bool(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float) arrives in fa0
	var v1 uint64 = ((p0) & uint64(0xffffffff))
	// a0: operand `b` (bool) zero-extended
	var v2 uint64 = ((p1) & uint64(0x1))
	var v3 uint64 = emul.Emu_ui32_to_f32_rm0(uint32(v2))
	var v4 uint64 = emul.Emu_f32_sub_rm0(v1, v3)
	return ((v4) & uint64(0xffffffff))
}
