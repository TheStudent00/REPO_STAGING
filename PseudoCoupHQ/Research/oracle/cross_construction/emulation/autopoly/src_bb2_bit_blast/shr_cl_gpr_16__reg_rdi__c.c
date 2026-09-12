/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of shr_cl_gpr_16__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 16, v0), LShR(Extract(15, 0, v0), Concat(0, Extract(4, 0, v1)))) */
#include <stdint.h>

uint64_t
emu_shr_cl_gpr_16__reg_rdi__c(uint64_t a, uint8_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(((uint64_t)((uint64_t)a >> 16) & UINT64_C(0xffffffffffff))) << 16) | (uint64_t)((((uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0xffff))) < (uint32_t)16) ? ((uint32_t)((uint32_t)(((uint32_t)((uint64_t)a >> 0) & UINT32_C(0xffff))) >> (unsigned)(uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0xffff)))) & UINT32_C(0xffff)) : (uint32_t)0))));
}
