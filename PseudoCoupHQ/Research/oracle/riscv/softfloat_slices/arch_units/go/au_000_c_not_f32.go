// arch-unit 0  --  c  `!a`  lhs=float rhs=None
// symbol op_3   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_000_c_not_f32(p0 uint64) uint64 {
	// fa0: operand `a` (float) arrives in fa0
	var v1 uint64 = ((p0) & uint64(0xffffffff))
	var v2 uint64 = ((uint64(0x0)) & uint64(0xffffffff))
	var v3 uint64 = b2u(emul.Emu_f32_eq_rm0(v1, v2))
	return v3
}
