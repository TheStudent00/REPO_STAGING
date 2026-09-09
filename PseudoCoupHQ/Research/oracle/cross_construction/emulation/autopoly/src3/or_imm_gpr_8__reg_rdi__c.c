/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of or_imm_gpr_8__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(7, 2, v0), 3) */
#include <stdint.h>

uint64_t
emu_or_imm_gpr_8__reg_rdi__c(uint8_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 8) | ((uint64_t)(((uint32_t)((uint32_t)a >> 2) & UINT32_C(0x3f))) << 2) | (uint64_t)(UINT32_C(0x3))));
}
