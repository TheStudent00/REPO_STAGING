// arch-unit 42  --  c  `a - b`  lhs=double rhs=int32_t
// symbol op_162   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.w fa5, a0                   float    emulation:i32_to_f64_rm0
//   fsub.d fa0, fa0, fa5, dyn          float    emulation:f64_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_042_c_neg_f64_i32(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (double) arrives in fa0
	var v1 uint64 = p0
	// a0: operand `b` (int32_t) sign-extended to XLEN
	var v2 uint64 = uint64(int64(int32(uint32(p1))))
	var v3 uint64 = emul.Emu_i32_to_f64_rm0(uint32(v2))
	var v4 uint64 = emul.Emu_f64_sub_rm0(v1, v3)
	return v4
}
