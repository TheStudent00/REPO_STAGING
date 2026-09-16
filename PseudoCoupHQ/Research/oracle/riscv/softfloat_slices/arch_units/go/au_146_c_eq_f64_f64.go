// arch-unit 146  --  c  `a == b`  lhs=double rhs=double
// symbol op_490   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   feq.d a0, fa0, fa1                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_146_c_eq_f64_f64(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (double) arrives in fa0
	var v1 uint64 = p0
	// fa1: operand `b` (double) arrives in fa1
	var v2 uint64 = p1
	var v3 uint64 = b2u(emul.Emu_f64_eq_rm0(v1, v2))
	return v3
}
