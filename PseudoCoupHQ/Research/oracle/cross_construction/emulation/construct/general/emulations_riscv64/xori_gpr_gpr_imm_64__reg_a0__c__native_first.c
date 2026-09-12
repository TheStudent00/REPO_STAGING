/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of xori_gpr_gpr_imm_64__reg_a0__c__native_first.  The term's text, LITERAL:
   Concat(Extract(63, 2, v0), ~Extract(1, 0, v0)) */
#include <stdint.h>

uint64_t
emu_xori_gpr_gpr_imm_64__reg_a0__c__native_first(uint64_t a)
{
    uint32_t v0 = ((uint32_t)((uint64_t)a >> 0) & UINT32_C(0x3));
    uint32_t v1 = ((uint32_t)(~(uint32_t)(v0)) & UINT32_C(0x3));
    uint64_t v2 = ((uint64_t)((uint64_t)a >> 2) & UINT64_C(0x3fffffffffffffff));
    uint64_t v3 = (uint64_t)(((uint64_t)(v2) << 2) | (uint64_t)(v1));
    return (uint64_t)(v3);
}
