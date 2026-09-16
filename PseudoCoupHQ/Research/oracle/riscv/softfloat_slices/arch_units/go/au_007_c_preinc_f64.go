// arch-unit 7  --  c  `++a`  lhs=double rhs=None
// symbol op_40   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fli.d fa5, 1.0                     float    bit-manipulation
//   fadd.d fa0, fa0, fa5, dyn          float    emulation:f64_add_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_007_c_preinc_f64(p0 uint64) uint64 {
	// fa0: operand `a` (double) arrives in fa0
	var v1 uint64 = p0
	var v2 uint64 = uint64(0x3ff0000000000000)
	var v3 uint64 = emul.Emu_f64_add_rm0(v1, v2)
	return v3
}
