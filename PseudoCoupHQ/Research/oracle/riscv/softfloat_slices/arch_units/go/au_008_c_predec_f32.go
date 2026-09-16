// arch-unit 8  --  c  `--a`  lhs=float rhs=None
// symbol op_45   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fli.s fa5, -1.0                    float    bit-manipulation
//   fadd.s fa0, fa0, fa5, dyn          float    emulation:f32_add_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_008_c_predec_f32(p0 uint64) uint64 {
	// fa0: operand `a` (float) arrives in fa0
	var v1 uint64 = ((p0) & uint64(0xffffffff))
	var v2 uint64 = uint64(0xbf800000)
	var v3 uint64 = emul.Emu_f32_add_rm0(v1, v2)
	return ((v3) & uint64(0xffffffff))
}
