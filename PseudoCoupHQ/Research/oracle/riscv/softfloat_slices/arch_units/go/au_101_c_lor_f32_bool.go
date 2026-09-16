// arch-unit 101  --  c  `a || b`  lhs=float rhs=bool
// symbol op_305   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a1, fa0, fa5                 float    emulation:f32_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   c.or a0, a1                        integer  operator:|
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_101_c_lor_f32_bool(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float) arrives in fa0
	var v1 uint64 = ((p0) & uint64(0xffffffff))
	// a0: operand `b` (bool) zero-extended
	var v2 uint64 = ((p1) & uint64(0x1))
	var v3 uint64 = ((uint64(0x0)) & uint64(0xffffffff))
	var v4 uint64 = b2u(emul.Emu_f32_eq_rm0(v1, v3))
	var v5 uint64 = ((v4) ^ uint64(0x1))
	var v6 uint64 = ((v2) | (v5))
	return v6
}
