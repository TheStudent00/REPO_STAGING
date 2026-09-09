/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of sar_cl_gpr_32__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1))) */
#include <stdint.h>

uint64_t
emu_sar_cl_gpr_32__reg_rdi__c(uint32_t a, uint8_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((int32_t)((uint32_t)a) >> (unsigned)(uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))))))));
}
