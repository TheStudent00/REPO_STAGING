/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of slli_gpr_gpr_imm_64__reg_a0__c__all_constructed.  The term's text, LITERAL:
   Concat(Extract(60, 0, v0), 0) */
#include <stdint.h>

uint64_t
emu_slli_gpr_gpr_imm_64__reg_a0__c__all_constructed(uint64_t a)
{
    uint64_t v0 = ((uint64_t)((uint64_t)a >> 0) & UINT64_C(0x1fffffffffffffff));
    uint32_t v1 = UINT32_C(0x0);
    uint64_t v2 = v0;
    uint64_t v3 = (uint64_t)(((uint64_t)(v2) << 3) | (uint64_t)(v1));
    return (uint64_t)(v3);
}
