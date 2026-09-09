/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of sbb_gpr_same_32__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, If(Extract(32, 32, Concat(0, Extract(31, 0, v0)) + Concat(0, Extract(31, 0, v1))) == 1, 1, 0)*4294967295) */
#include <stdint.h>

uint64_t
emu_sbb_gpr_same_32__reg_rdi__c(uint32_t a, uint32_t b, uint64_t c)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((uint32_t)(((((uint32_t)(((uint32_t)((uint64_t)(((uint64_t)((uint64_t)(((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)b)) & UINT64_C(0x1ffffffff))) + (uint64_t)(((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)a)) & UINT64_C(0x1ffffffff)))) & UINT64_C(0x1ffffffff))) >> 32) & UINT32_C(0x1))) == (uint32_t)(UINT32_C(0x1)))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0)))) * (uint32_t)(UINT32_C(0xffffffff))))));
}
