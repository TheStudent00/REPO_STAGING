// arch-unit 120  --  c  `a && b`  lhs=float rhs=double
// symbol op_340   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa1, fa5                 float    emulation:f64_eq_rm0
//   c.or a0, a1                        integer  operator:|
//   xori a0, a0, 0x1                   integer  operator:^
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_120_c_land_f32_f64(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (float) arrives in fa0
	var v1 uint64 = ((p0) & uint64(0xffffffff))
	// fa1: operand `b` (double) arrives in fa1
	var v2 uint64 = p1
	var v3 uint64 = ((uint64(0x0)) & uint64(0xffffffff))
	var v4 uint64 = b2u(emul.Emu_f32_eq_rm0(v1, v3))
	var v5 uint64 = uint64(0x0)
	var v6 uint64 = b2u(emul.Emu_f64_eq_rm0(v2, v5))
	var v7 uint64 = ((v4) | (v6))
	var v8 uint64 = ((v7) ^ uint64(0x1))
	return v8
}
