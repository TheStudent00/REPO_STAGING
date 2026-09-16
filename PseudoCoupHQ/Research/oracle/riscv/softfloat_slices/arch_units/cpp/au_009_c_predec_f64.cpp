// arch-unit 9  --  c  `--a`  lhs=double rhs=None
// symbol op_46   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fli.d fa5, -1.0                    float    bit-manipulation
//   fadd.d fa0, fa0, fa5, dyn          float    emulation:f64_add_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_009_c_predec_f64(uint64_t p0)
{
    /* fa0: operand `a` (double) arrives in fa0 */
    const uint64_t v1 = p0;
    const uint64_t v2 = UINT64_C(0xbff0000000000000);
    const uint64_t v3 = sfemul::f64_add_rm0(v1, v2);
    return v3;
}

}  // namespace archunits
