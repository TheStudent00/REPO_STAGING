/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of shr_cl_gpr_64__reg_rdi__c.  The term's layer-5 text, LITERAL:
   LShR(v0, Concat(0, Extract(5, 0, v1))) */
#include <stdint.h>

uint64_t
emu_shr_cl_gpr_64__reg_rdi__c(uint64_t a, uint8_t b)
{
    return (uint64_t)((uint64_t)((uint64_t)((uint64_t)a) >> (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x3f)))))));
}
