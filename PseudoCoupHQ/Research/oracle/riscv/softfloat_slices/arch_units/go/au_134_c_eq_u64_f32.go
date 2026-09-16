// arch-unit 134  --  c  `a == b`  lhs=uint64_t rhs=float
// symbol op_477   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.lu fa5, a0, dyn             float    emulation:ui64_to_f32_rm0
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_134_c_eq_u64_f32(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (uint64_t) arrives in a0
	var v1 uint64 = p0
	// fa0: operand `b` (float) arrives in fa0
	var v2 uint64 = ((p1) & uint64(0xffffffff))
	var v3 uint64 = emul.Emu_ui64_to_f32_rm0(v1)
	var v4 uint64 = b2u(emul.Emu_f32_eq_rm0(v2, v3))
	return v4
}
