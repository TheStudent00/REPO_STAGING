// arch-unit 163  --  go  `a == b`  lhs=float64 rhs=float64
// symbol main.op_484   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   feq.d a0, fa0, fa1                 float    emulation:f64_eq_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_163_go_eq_f64_f64(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float64) arrives in fa0
	var v1 uint64 = p0
	// fa1: operand `b` (float64) arrives in fa1
	var v2 uint64 = p1
	var v3 uint64 = b2u(emul.Emu_f64_eq_rm0(v1, v2))
	return v3
}
