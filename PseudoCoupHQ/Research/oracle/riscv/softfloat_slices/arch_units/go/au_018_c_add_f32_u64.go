// arch-unit 18  --  c  `a + b`  lhs=float rhs=uint64_t
// symbol op_122   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.lu fa5, a0, dyn             float    emulation:ui64_to_f32_rm0
//   fadd.s fa0, fa0, fa5, dyn          float    emulation:f32_add_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_018_c_add_f32_u64(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float) arrives in fa0
	var v1 uint64 = ((p0) & uint64(0xffffffff))
	// a0: operand `b` (uint64_t) arrives in a0
	var v2 uint64 = p1
	var v3 uint64 = emul.Emu_ui64_to_f32_rm0(v2)
	var v4 uint64 = emul.Emu_f32_add_rm0(v1, v3)
	return ((v4) & uint64(0xffffffff))
}
