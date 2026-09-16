// arch-unit 160  --  go  `a - b`  lhs=float32 rhs=float32
// symbol main.op_369   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsub.s fa0, fa0, fa1, rne          float    emulation:f32_sub_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_160_go_neg_f32_f32(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float32) arrives in fa0
	var v1 uint64 = ((p0) & uint64(0xffffffff))
	// fa1: operand `b` (float32) arrives in fa1
	var v2 uint64 = ((p1) & uint64(0xffffffff))
	var v3 uint64 = emul.Emu_f32_sub_rm0(v1, v2)
	return ((v3) & uint64(0xffffffff))
}
