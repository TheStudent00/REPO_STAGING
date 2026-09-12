/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of srai_gpr_gpr_imm_64__reg_a0__c__native_first.  The term's text, LITERAL:
   v0 >> 3 */
#include <stdint.h>

uint64_t
emu_srai_gpr_gpr_imm_64__reg_a0__c__native_first(uint64_t a)
{
    uint64_t v0 = (uint64_t)((int64_t)((uint64_t)a) >> (unsigned)(uint64_t)(UINT64_C(0x3)));
    return (uint64_t)(v0);
}
