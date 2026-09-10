/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of div_gpr_gpr_gpr_64__reg_a0__c.  The term's layer-5 text, LITERAL:
   If(v0 == 0, 18446744073709551615, If(And(v0 == 18446744073709551615, v1 == 9223372036854775808), 9223372036854775808, bvsdiv_i(v1, v0))) */
#include <stdint.h>

uint64_t
emu_div_gpr_gpr_gpr_64__reg_a0__c(uint64_t a, uint64_t b)
{
    return (uint64_t)(((((uint64_t)((uint64_t)a) == (uint64_t)(UINT64_C(0x0)))) ? (uint64_t)(UINT64_C(0xffffffffffffffff)) : (uint64_t)(((((((uint64_t)((uint64_t)a) == (uint64_t)(UINT64_C(0xffffffffffffffff)))) && (((uint64_t)((uint64_t)b) == (uint64_t)(UINT64_C(0x8000000000000000)))))) ? (uint64_t)(UINT64_C(0x8000000000000000)) : (uint64_t)((uint64_t)((int64_t)((int64_t)((uint64_t)b)) / (int64_t)((int64_t)((uint64_t)a))))))));
}
