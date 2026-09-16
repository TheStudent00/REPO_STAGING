// arch-unit 99  --  c  `a || b`  lhs=float rhs=float
// symbol op_303   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   feq.s a1, fa1, fa5                 float    emulation:f32_eq_rm0
//   c.and a0, a1                       integer  operator:&
//   xori a0, a0, 0x1                   integer  operator:^
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_099_c_lor_f32_f32(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float) arrives in fa0
	var v1 uint64 = ((p0) & uint64(0xffffffff))
	// fa1: operand `b` (float) arrives in fa1
	var v2 uint64 = ((p1) & uint64(0xffffffff))
	var v3 uint64 = ((uint64(0x0)) & uint64(0xffffffff))
	var v4 uint64 = b2u(emul.Emu_f32_eq_rm0(v1, v3))
	var v5 uint64 = b2u(emul.Emu_f32_eq_rm0(v2, v3))
	var v6 uint64 = ((v4) & (v5))
	var v7 uint64 = ((v6) ^ uint64(0x1))
	return v7
}
