// arch-unit 102  --  c  `a || b`  lhs=double rhs=int32_t
// symbol op_306   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   sltu a0, zero, a0                  integer  operator:<
//   c.or a0, a1                        integer  operator:|
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_102_c_lor_f64_i32(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (double) arrives in fa0
	var v1 uint64 = p0
	// a0: operand `b` (int32_t) sign-extended to XLEN
	var v2 uint64 = uint64(int64(int32(uint32(p1))))
	var v3 uint64 = uint64(0x0)
	var v4 uint64 = b2u(emul.Emu_f64_eq_rm0(v1, v3))
	var v5 uint64 = ((v4) ^ uint64(0x1))
	var v6 uint64 = b2u((uint64(0x0)) < (v2))
	var v7 uint64 = ((v6) | (v5))
	return v7
}
