// arch-unit 92  --  c  `a || b`  lhs=int64_t rhs=float
// symbol op_291   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                  integer  operator:<
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a1, fa0, fa5                 float    emulation:f32_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   c.or a0, a1                        integer  operator:|
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_092_c_lor_i64_f32(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (int64_t) arrives in a0
	var v1 uint64 = p0
	// fa0: operand `b` (float) arrives in fa0
	var v2 uint64 = ((p1) & uint64(0xffffffff))
	var v3 uint64 = b2u((uint64(0x0)) < (v1))
	var v4 uint64 = ((uint64(0x0)) & uint64(0xffffffff))
	var v5 uint64 = b2u(emul.Emu_f32_eq_rm0(v2, v4))
	var v6 uint64 = ((v5) ^ uint64(0x1))
	var v7 uint64 = ((v3) | (v6))
	return v7
}
