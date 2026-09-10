/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of or_gpr_gpr_16__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(15, 0, v0) | Extract(15, 0, v1)) */
#include <stdint.h>

uint64_t
emu_or_gpr_gpr_16__reg_rdi__c(uint16_t a, uint16_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 16) | (uint64_t)(((uint32_t)((uint32_t)((uint32_t)a) | (uint32_t)((uint32_t)b)) & UINT32_C(0xffff)))));
}
