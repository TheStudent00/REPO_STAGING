/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of srl_gpr_gpr_same_64__reg_a0__c.  The term's layer-5 text, LITERAL:
   LShR(v0, Concat(0, Extract(5, 0, v0))) */
#include <stdint.h>

uint64_t
emu_srl_gpr_gpr_same_64__reg_a0__c(uint64_t a)
{
    return (uint64_t)((uint64_t)((uint64_t)((uint64_t)a) >> (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((uint32_t)((uint64_t)a >> 0) & UINT32_C(0x3f)))))));
}
