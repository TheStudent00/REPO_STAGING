// arch-unit 4  --  c  `&a`  lhs=float rhs=None
// symbol op_33   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.addi sp, -0x10                   integer  address/stack/runtime -- not a bit function
//   c.addi4spn a0, sp, 0xc             integer  address/stack/runtime -- not a bit function
//   fsw fa0, 0xc(sp)                   float    bit-manipulation
//   c.addi sp, 0x10                    integer  address/stack/runtime -- not a bit function
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
//
// REDUCED: `&a` yields an address, which is not a function of the
// operand bits.  What is emulated and verified here is *(&a): the
// bit pattern the float store/load arch-opcode moves.
package archunits

func Au_004_c_addr_f32(p0 uint64) uint64 {
	return ((p0) & uint64(0xffffffff))
}
