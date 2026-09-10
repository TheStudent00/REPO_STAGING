/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of slti_gpr_gpr_imm_64__reg_a0__c.  The term's layer-5 text, LITERAL:
   If(3 <= v0, 0, 1) */
#include <stdint.h>

uint64_t
emu_slti_gpr_gpr_imm_64__reg_a0__c(uint64_t a)
{
    return (uint64_t)(((((int64_t)(UINT64_C(0x3)) <= (int64_t)((uint64_t)a))) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)(UINT64_C(0x1))));
}
