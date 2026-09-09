/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of div_gpr_one_32__reg_rax__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 0, bvudiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(0, Extract(31, 0, v2))))) */
#include <stdint.h>

uint64_t
emu_div_gpr_one_32__reg_rax__c(uint32_t a, uint32_t b, uint32_t c)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((uint64_t)((uint64_t)((uint64_t)((uint64_t)(((uint64_t)((uint32_t)a) << 32) | (uint64_t)((uint32_t)b))) / (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)c))))) >> 0))));
}
