/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of or_gpr_gpr_8__reg_rdi__c__all_constructed.  The term's text, LITERAL:
   Concat(Extract(63, 8, v0), Extract(7, 0, v0) | Extract(7, 0, v1)) */
#include <stdint.h>

uint64_t
emu_or_gpr_gpr_8__reg_rdi__c__all_constructed(uint64_t a, uint8_t b)
{
    uint32_t v0 = (uint32_t)b;
    uint32_t v1 = ((uint32_t)((uint64_t)a >> 0) & UINT32_C(0xff));
    uint32_t v2 = ((uint32_t)((uint32_t)(v1) | (uint32_t)(v0)) & UINT32_C(0xff));
    uint64_t v3 = ((uint64_t)((uint64_t)a >> 8) & UINT64_C(0xffffffffffffff));
    uint32_t v4 = v2;
    uint64_t v5 = v3;
    uint64_t v6 = (uint64_t)(((uint64_t)(v5) << 8) | (uint64_t)(v4));
    return (uint64_t)(v6);
}
