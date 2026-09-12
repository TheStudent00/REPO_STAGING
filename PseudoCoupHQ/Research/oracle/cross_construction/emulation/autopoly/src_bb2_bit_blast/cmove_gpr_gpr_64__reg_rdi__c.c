/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of cmove_gpr_gpr_64__reg_rdi__c.  The term's layer-5 text, LITERAL:
   If(~(~Extract(63, 0, v0) | ~v1) == 0, v2, v3) */
#include <stdint.h>

uint64_t
emu_cmove_gpr_gpr_64__reg_rdi__c(uint64_t a, uint64_t b, uint64_t c, uint64_t d)
{
    return (uint64_t)(((((uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)((uint64_t)(~(uint64_t)((uint64_t)b))) | (uint64_t)((uint64_t)(~(uint64_t)((uint64_t)a))))))) == (uint64_t)(UINT64_C(0x0)))) ? (uint64_t)((uint64_t)c) : (uint64_t)((uint64_t)d)));
}
