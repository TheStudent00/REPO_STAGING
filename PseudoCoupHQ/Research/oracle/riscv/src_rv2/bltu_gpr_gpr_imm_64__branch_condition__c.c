/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of bltu_gpr_gpr_imm_64__branch_condition__c.  The term's layer-5 text, LITERAL:
   If(ULE(v0, v1), 0, 1) */
#include <stdint.h>

uint64_t
emu_bltu_gpr_gpr_imm_64__branch_condition__c(uint64_t a, uint64_t b)
{
    return (uint64_t)(((((uint64_t)((uint64_t)b) <= (uint64_t)((uint64_t)a))) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)(UINT64_C(0x1))));
}
