// arch-unit 173  --  go  `a >= b`  lhs=float64 rhs=float64
// symbol main.op_664   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fle.d a0, fa1, fa0                 float    emulation:f64_le_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_173_go_ge_f64_f64(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float64) arrives in fa0
	var v1 uint64 = p0
	// fa1: operand `b` (float64) arrives in fa1
	var v2 uint64 = p1
	var v3 uint64 = b2u(emul.Emu_f64_le_rm0(v2, v1))
	return v3
}
