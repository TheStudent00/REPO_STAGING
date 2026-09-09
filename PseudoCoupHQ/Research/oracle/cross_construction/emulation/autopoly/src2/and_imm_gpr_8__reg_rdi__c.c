/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of and_imm_gpr_8__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(1, 0, v0)) */
#include <stdint.h>

uint64_t
emu_and_imm_gpr_8__reg_rdi__c(uint8_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 2) | (uint64_t)(((uint32_t)((uint32_t)a >> 0) & UINT32_C(0x3)))));
}
