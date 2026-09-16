// arch-unit 3  --  c  `-a`  lhs=double rhs=None
// symbol op_16   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsgnjn.d fa0, fa0, fa0             float    bit-manipulation
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
package archunits

func Au_003_c_neg_f64(p0 uint64) uint64 {
	// fa0: operand `a` (double) arrives in fa0
	var v1 uint64 = p0
	var v2 uint64 = (((v1) & uint64(0x7fffffffffffffff)) | ((^(v1)) & uint64(0x8000000000000000)))
	return v2
}
