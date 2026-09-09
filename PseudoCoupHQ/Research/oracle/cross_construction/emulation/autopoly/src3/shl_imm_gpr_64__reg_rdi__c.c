/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of shl_imm_gpr_64__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(60, 0, v0), 0) */
#include <stdint.h>

uint64_t
emu_shl_imm_gpr_64__reg_rdi__c(uint64_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)(((uint64_t)((uint64_t)a >> 0) & UINT64_C(0x1fffffffffffffff))) << 3) | (uint64_t)(UINT32_C(0x0))));
}
