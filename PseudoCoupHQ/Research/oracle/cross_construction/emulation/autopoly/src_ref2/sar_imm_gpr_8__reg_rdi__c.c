/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of sar_imm_gpr_8__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 8, v0), Extract(7, 0, v0) >> 3) */
#include <stdint.h>

uint64_t
emu_sar_imm_gpr_8__reg_rdi__c(uint64_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)(((uint64_t)((uint64_t)a >> 8) & UINT64_C(0xffffffffffffff))) << 8) | (uint64_t)(((uint32_t)(((int32_t)((uint32_t)(((uint32_t)((uint64_t)a >> 0) & UINT32_C(0xff))) << 24) >> 24) >> (unsigned)(uint32_t)(UINT32_C(0x3))) & UINT32_C(0xff)))));
}
