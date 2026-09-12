/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of sh_gpr_gpr_imm_16__mem_MEM_a1__c__native_first.  The term's text, LITERAL:
   Concat(Extract(63, 16, v0), Extract(15, 0, v1)) */
#include <stdint.h>

uint64_t
emu_sh_gpr_gpr_imm_16__mem_MEM_a1__c__native_first(uint64_t a, uint16_t b)
{
    uint32_t v0 = (uint32_t)b;
    uint64_t v1 = ((uint64_t)((uint64_t)a >> 16) & UINT64_C(0xffffffffffff));
    uint64_t v2 = (uint64_t)(((uint64_t)(v1) << 16) | (uint64_t)(v0));
    return (uint64_t)(v2);
}
