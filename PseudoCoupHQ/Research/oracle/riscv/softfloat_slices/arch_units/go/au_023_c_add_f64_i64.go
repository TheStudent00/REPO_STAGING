// arch-unit 23  --  c  `a + b`  lhs=double rhs=int64_t
// symbol op_127   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.l fa5, a0, dyn              float    emulation:i64_to_f64_rm0
//   fadd.d fa0, fa0, fa5, dyn          float    emulation:f64_add_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_023_c_add_f64_i64(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (double) arrives in fa0
	var v1 uint64 = p0
	// a0: operand `b` (int64_t) arrives in a0
	var v2 uint64 = p1
	var v3 uint64 = emul.Emu_i64_to_f64_rm0(v2)
	var v4 uint64 = emul.Emu_f64_add_rm0(v1, v3)
	return v4
}
