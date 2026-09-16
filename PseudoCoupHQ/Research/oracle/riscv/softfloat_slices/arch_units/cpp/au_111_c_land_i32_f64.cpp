// arch-unit 111  --  c  `a && b`  lhs=int32_t rhs=double
// symbol op_322   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                  integer  operator:<
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   c.and a0, a1                       integer  operator:&
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_111_c_land_i32_f64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int32_t) sign-extended to XLEN */
    const uint64_t v1 = (uint64_t)(int64_t)(int32_t)(uint32_t)(p0);
    /* fa0: operand `b` (double) arrives in fa0 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_b2u((UINT64_C(0x0)) < (v1));
    const uint64_t v4 = UINT64_C(0x0);
    const uint64_t v5 = au_b2u(sfemul::f64_eq_rm0(v2, v4));
    const uint64_t v6 = ((v5) ^ UINT64_C(0x1));
    const uint64_t v7 = ((v3) & (v6));
    return v7;
}

}  // namespace archunits
