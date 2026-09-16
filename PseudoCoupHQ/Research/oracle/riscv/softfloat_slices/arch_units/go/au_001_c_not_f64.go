// arch-unit 1  --  c  `!a`  lhs=double rhs=None
// symbol op_4   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_001_c_not_f64(p0 uint64) uint64 {
	// fa0: operand `a` (double) arrives in fa0
	var v1 uint64 = p0
	var v2 uint64 = uint64(0x0)
	var v3 uint64 = b2u(emul.Emu_f64_eq_rm0(v1, v2))
	return v3
}
