/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of setae_gpr_one_8__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 8, v0), If(ULE(Extract(7, 0, v1), Extract(7, 0, v2)), 1, 0)) */
#include <stdint.h>

uint64_t
emu_setae_gpr_one_8__reg_rdi__c(uint8_t a, uint8_t b, uint64_t c)
{
    return (uint64_t)((uint64_t)(((uint64_t)(((uint64_t)((uint64_t)c >> 8) & UINT64_C(0xffffffffffffff))) << 8) | (uint64_t)(((((uint32_t)((uint32_t)b) <= (uint32_t)((uint32_t)a))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0))))));
}
