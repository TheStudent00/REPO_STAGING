/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of lhu_gpr_gpr_16__reg_a0__c__all_constructed.  The term's text, LITERAL:
   Concat(0, Extract(15, 0, v0)) */
#include <stdint.h>

uint64_t
emu_lhu_gpr_gpr_16__reg_a0__c__all_constructed(uint16_t a)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = v0;
    uint64_t v2 = UINT64_C(0x0);
    uint64_t v3 = (uint64_t)(((uint64_t)(v2) << 16) | (uint64_t)(v1));
    return (uint64_t)(v3);
}
