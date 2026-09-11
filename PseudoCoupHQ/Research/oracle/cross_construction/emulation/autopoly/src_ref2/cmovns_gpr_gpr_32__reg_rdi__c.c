/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of cmovns_gpr_gpr_32__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, If(Or(Extract(31, 31, v0) == 0, Extract(31, 31, v1) == 0), Extract(31, 0, v2), Extract(31, 0, v3))) */
#include <stdint.h>

uint64_t
emu_cmovns_gpr_gpr_32__reg_rdi__c(uint32_t a, uint32_t b, uint32_t c, uint32_t d)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)(((((((uint32_t)(((uint32_t)((uint32_t)b >> 31) & UINT32_C(0x1))) == (uint32_t)(UINT32_C(0x0)))) || (((uint32_t)(((uint32_t)((uint32_t)a >> 31) & UINT32_C(0x1))) == (uint32_t)(UINT32_C(0x0)))))) ? (uint32_t)((uint32_t)c) : (uint32_t)((uint32_t)d)))));
}
