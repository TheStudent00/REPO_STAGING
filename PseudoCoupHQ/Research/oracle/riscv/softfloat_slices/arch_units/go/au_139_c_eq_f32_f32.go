// arch-unit 139  --  c  `a == b`  lhs=float rhs=float
// symbol op_483   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   feq.s a0, fa0, fa1                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_139_c_eq_f32_f32(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float) arrives in fa0
	var v1 uint64 = ((p0) & uint64(0xffffffff))
	// fa1: operand `b` (float) arrives in fa1
	var v2 uint64 = ((p1) & uint64(0xffffffff))
	var v3 uint64 = b2u(emul.Emu_f32_eq_rm0(v1, v2))
	return v3
}
