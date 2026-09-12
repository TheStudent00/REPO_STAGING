/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of sub_gpr_gpr_16__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 16, v0), Extract(15, 0, v1)*65535 + Extract(15, 0, v0)) */
#include <stdint.h>

uint64_t
emu_sub_gpr_gpr_16__reg_rdi__c(uint64_t a, uint16_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(((uint64_t)((uint64_t)a >> 16) & UINT64_C(0xffffffffffff))) << 16) | (uint64_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)((uint32_t)b) * (uint32_t)(UINT32_C(0xffff))) & UINT32_C(0xffff))) + (uint32_t)(((uint32_t)((uint64_t)a >> 0) & UINT32_C(0xffff)))) & UINT32_C(0xffff)))));
}
