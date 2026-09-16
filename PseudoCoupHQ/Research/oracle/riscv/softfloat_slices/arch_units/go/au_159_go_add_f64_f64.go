// arch-unit 159  --  go  `a + b`  lhs=float64 rhs=float64
// symbol main.op_340   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fadd.d fa0, fa0, fa1, rne          float    emulation:f64_add_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_159_go_add_f64_f64(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float64) arrives in fa0
	var v1 uint64 = p0
	// fa1: operand `b` (float64) arrives in fa1
	var v2 uint64 = p1
	var v3 uint64 = emul.Emu_f64_add_rm0(v1, v2)
	return v3
}
