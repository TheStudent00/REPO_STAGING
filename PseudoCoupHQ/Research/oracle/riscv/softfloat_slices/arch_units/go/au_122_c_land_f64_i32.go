// arch-unit 122  --  c  `a && b`  lhs=double rhs=int32_t
// symbol op_342   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   sltu a0, zero, a0                  integer  operator:<
//   andn a0, a0, a1                    integer  operator:& ~
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_122_c_land_f64_i32(p0 uint64, p1 uint64) uint64 {
	// fa0: operand `a` (double) arrives in fa0
	var v1 uint64 = p0
	// a0: operand `b` (int32_t) sign-extended to XLEN
	var v2 uint64 = uint64(int64(int32(uint32(p1))))
	var v3 uint64 = uint64(0x0)
	var v4 uint64 = b2u(emul.Emu_f64_eq_rm0(v1, v3))
	var v5 uint64 = b2u((uint64(0x0)) < (v2))
	var v6 uint64 = ((v5) & (^(v4)))
	return v6
}
