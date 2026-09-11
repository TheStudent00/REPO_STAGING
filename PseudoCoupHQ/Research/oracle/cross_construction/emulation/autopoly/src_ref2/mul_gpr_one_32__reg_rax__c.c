/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of mul_gpr_one_32__reg_rax__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 0, v0)*Extract(31, 0, v1)) */
#include <stdint.h>

uint64_t
emu_mul_gpr_one_32__reg_rax__c(uint32_t a, uint32_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((uint32_t)((uint32_t)a) * (uint32_t)((uint32_t)b)))));
}
