// arch-unit 31  --  c  `a - b`  lhs=int32_t rhs=double
// symbol op_142   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.w fa5, a0                   float    emulation:i32_to_f64_rm0
//   fsub.d fa0, fa5, fa0, dyn          float    emulation:f64_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_031_c_neg_i32_f64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int32_t) sign-extended to XLEN
	var v1 uint64 = uint64(int64(int32(uint32(p0))))
	// fa0: operand `b` (double) arrives in fa0
	var v2 uint64 = p1
	var v3 uint64 = emul.Emu_i32_to_f64_rm0(uint32(v1))
	var v4 uint64 = emul.Emu_f64_sub_rm0(v3, v2)
	return v4
}
