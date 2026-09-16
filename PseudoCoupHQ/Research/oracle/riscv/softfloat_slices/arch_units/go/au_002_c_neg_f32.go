// arch-unit 2  --  c  `-a`  lhs=float rhs=None
// symbol op_15   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsgnjn.s fa0, fa0, fa0             float    bit-manipulation
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
package archunits

func Au_002_c_neg_f32(p0 uint64) uint64 {
	// fa0: operand `a` (float) arrives in fa0
	var v1 uint64 = ((p0) & uint64(0xffffffff))
	var v2 uint64 = (((v1) & uint64(0x7fffffff)) | ((^(v1)) & uint64(0x80000000)))
	return ((v2) & uint64(0xffffffff))
}
