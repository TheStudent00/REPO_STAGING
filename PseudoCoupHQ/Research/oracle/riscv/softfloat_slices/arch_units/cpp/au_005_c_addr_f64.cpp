// arch-unit 5  --  c  `&a`  lhs=double rhs=None
// symbol op_34   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.addi sp, -0x10                   integer  address/stack/runtime -- not a bit function
//   c.addi4spn a0, sp, 0x8             integer  address/stack/runtime -- not a bit function
//   c.fsdsp fa0, 0x8(sp)               float    bit-manipulation
//   c.addi sp, 0x10                    integer  address/stack/runtime -- not a bit function
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
//
// REDUCED: `&a` yields an address, which is not a function of the
// operand bits.  What is emulated and verified here is *(&a): the
// bit pattern the float store/load arch-opcode moves.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_005_c_addr_f64(uint64_t p0)
{
    return p0;
}

}  // namespace archunits
