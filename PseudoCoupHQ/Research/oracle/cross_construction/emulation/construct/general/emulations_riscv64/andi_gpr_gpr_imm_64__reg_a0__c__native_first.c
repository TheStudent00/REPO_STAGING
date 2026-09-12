/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of andi_gpr_gpr_imm_64__reg_a0__c__native_first.  The term's text, LITERAL:
   Concat(0, Extract(1, 0, v0)) */
#include <stdint.h>

uint64_t
emu_andi_gpr_gpr_imm_64__reg_a0__c__native_first(uint8_t a)
{
    uint32_t v0 = ((uint32_t)((uint32_t)a >> 0) & UINT32_C(0x3));
    uint64_t v1 = (uint64_t)(((uint64_t)(UINT64_C(0x0)) << 2) | (uint64_t)(v0));
    return (uint64_t)(v1);
}
