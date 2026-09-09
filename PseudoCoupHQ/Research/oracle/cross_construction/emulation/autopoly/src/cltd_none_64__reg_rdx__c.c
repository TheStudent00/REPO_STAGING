/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of cltd_none_64__reg_rdx__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 0, v0) >> 31) */
#include <stdint.h>

uint64_t
emu_cltd_none_64__reg_rdx__c(uint32_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((int32_t)((uint32_t)a) >> (unsigned)(uint32_t)(UINT32_C(0x1f))))));
}
