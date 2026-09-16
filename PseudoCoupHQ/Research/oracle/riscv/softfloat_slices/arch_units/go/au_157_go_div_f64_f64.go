// arch-unit 157  --  go  `a / b`  lhs=float64 rhs=float64
// symbol main.op_124   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fdiv.d fa0, fa0, fa1, rne          float    emulation:f64_div_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_157_go_div_f64_f64(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float64) arrives in fa0
	var v1 uint64 = p0
	// fa1: operand `b` (float64) arrives in fa1
	var v2 uint64 = p1
	var v3 uint64 = emul.Emu_f64_div_rm0(v1, v2)
	return v3
}
