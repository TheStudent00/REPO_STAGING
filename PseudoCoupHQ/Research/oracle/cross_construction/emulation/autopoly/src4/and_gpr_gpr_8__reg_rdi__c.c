/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of and_gpr_gpr_8__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, ~(~Extract(7, 0, v0) | ~Extract(7, 0, v1))) */
#include <stdint.h>

uint64_t
emu_and_gpr_gpr_8__reg_rdi__c(uint8_t a, uint8_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 8) | (uint64_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)((uint32_t)a)) & UINT32_C(0xff))) | (uint32_t)(((uint32_t)(~(uint32_t)((uint32_t)b)) & UINT32_C(0xff)))) & UINT32_C(0xff)))) & UINT32_C(0xff)))));
}
