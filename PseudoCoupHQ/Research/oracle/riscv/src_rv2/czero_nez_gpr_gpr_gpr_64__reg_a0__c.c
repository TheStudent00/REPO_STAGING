/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of czero_nez_gpr_gpr_gpr_64__reg_a0__c.  The term's layer-5 text, LITERAL:
   If(v0 == 0, v1, 0) */
#include <stdint.h>

uint64_t
emu_czero_nez_gpr_gpr_gpr_64__reg_a0__c(uint64_t a, uint64_t b)
{
    return (uint64_t)(((((uint64_t)((uint64_t)a) == (uint64_t)(UINT64_C(0x0)))) ? (uint64_t)((uint64_t)b) : (uint64_t)(UINT64_C(0x0))));
}
