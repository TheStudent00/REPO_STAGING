/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of bge_gpr_gpr_64__branch_condition__c.  The term's layer-5 text, LITERAL:
   If(v0 <= v1, 1, 0) */
#include <stdint.h>

uint64_t
emu_bge_gpr_gpr_64__branch_condition__c(uint64_t a, uint64_t b)
{
    return (uint64_t)(((((int64_t)((uint64_t)b) <= (int64_t)((uint64_t)a))) ? (uint64_t)(UINT64_C(0x1)) : (uint64_t)(UINT64_C(0x0))));
}
