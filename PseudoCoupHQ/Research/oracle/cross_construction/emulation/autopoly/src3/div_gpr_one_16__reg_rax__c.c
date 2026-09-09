/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of div_gpr_one_16__reg_rax__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 16, v1), Extract(15, 0, bvudiv_i(Concat(Extract(15, 0, v0), Extract(15, 0, v1)), Concat(0, Extract(15, 0, v2))))) */
#include <stdint.h>

uint64_t
emu_div_gpr_one_16__reg_rax__c(uint16_t a, uint64_t b, uint16_t c)
{
    return (uint64_t)((uint64_t)(((uint64_t)(((uint64_t)((uint64_t)b >> 16) & UINT64_C(0xffffffffffff))) << 16) | (uint64_t)(((uint32_t)((uint32_t)((uint32_t)((uint32_t)((uint32_t)(((uint32_t)((uint32_t)a) << 16) | (uint32_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0xffff))))) / (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)((uint32_t)c))))) >> 0) & UINT32_C(0xffff)))));
}
