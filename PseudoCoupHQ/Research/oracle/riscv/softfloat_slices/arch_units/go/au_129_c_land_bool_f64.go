// arch-unit 129  --  c  `a && b`  lhs=bool rhs=double
// symbol op_352   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   c.and a0, a1                       integer  operator:&
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
package archunits

import emul "softfloat_emul"

func Au_129_c_land_bool_f64(p0 uint64, p1 uint64) uint64 {
	// a0: operand `a` (bool) zero-extended
	var v1 uint64 = ((p0) & uint64(0x1))
	// fa0: operand `b` (double) arrives in fa0
	var v2 uint64 = p1
	var v3 uint64 = uint64(0x0)
	var v4 uint64 = b2u(emul.Emu_f64_eq_rm0(v2, v3))
	var v5 uint64 = ((v4) ^ uint64(0x1))
	var v6 uint64 = ((v1) & (v5))
	return v6
}
