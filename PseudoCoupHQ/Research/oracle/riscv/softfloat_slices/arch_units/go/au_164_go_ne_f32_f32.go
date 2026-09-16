// arch-unit 164  --  go  `a != b`  lhs=float32 rhs=float32
// symbol main.op_513   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   feq.s a0, fa0, fa1                 float    emulation:f32_eq_rm0
//   xori a0, a0, 0x1                   integer  operator:^
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_164_go_ne_f32_f32(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float32) arrives in fa0
	var v1 uint64 = ((p0) & uint64(0xffffffff))
	// fa1: operand `b` (float32) arrives in fa1
	var v2 uint64 = ((p1) & uint64(0xffffffff))
	var v3 uint64 = b2u(emul.Emu_f32_eq_rm0(v1, v2))
	var v4 uint64 = ((v3) ^ uint64(0x1))
	return v4
}
