/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of shr_imm_gpr_32__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 3, v0)) */
#include <stdint.h>

uint64_t
emu_shr_imm_gpr_32__reg_rdi__c(uint32_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 29) | (uint64_t)(((uint32_t)((uint32_t)a >> 3) & UINT32_C(0x1fffffff)))));
}
