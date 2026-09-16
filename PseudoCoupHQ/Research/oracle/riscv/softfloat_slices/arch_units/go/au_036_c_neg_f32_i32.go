// arch-unit 36  --  c  `a - b`  lhs=float rhs=int32_t
// symbol op_156   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.w fa5, a0, dyn              float    emulation:i32_to_f32_rm0
//   fsub.s fa0, fa0, fa5, dyn          float    emulation:f32_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_036_c_neg_f32_i32(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float) arrives in fa0
	var v1 uint64 = ((p0) & uint64(0xffffffff))
	// a0: operand `b` (int32_t) sign-extended to XLEN
	var v2 uint64 = uint64(int64(int32(uint32(p1))))
	var v3 uint64 = emul.Emu_i32_to_f32_rm0(uint32(v2))
	var v4 uint64 = emul.Emu_f32_sub_rm0(v1, v3)
	return ((v4) & uint64(0xffffffff))
}
