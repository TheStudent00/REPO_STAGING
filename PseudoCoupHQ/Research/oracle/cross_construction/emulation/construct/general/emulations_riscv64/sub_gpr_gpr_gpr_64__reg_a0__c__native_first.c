/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of sub_gpr_gpr_gpr_64__reg_a0__c__native_first.  The term's text, LITERAL:
   v0*18446744073709551615 + v1 */
#include <stdint.h>

uint64_t
emu_sub_gpr_gpr_gpr_64__reg_a0__c__native_first(uint64_t a, uint64_t b)
{
    uint64_t v0 = (uint64_t)((uint64_t)((uint64_t)b) * (uint64_t)(UINT64_C(0xffffffffffffffff)));
    uint64_t v1 = (uint64_t)((uint64_t)(v0) + (uint64_t)((uint64_t)a));
    return (uint64_t)(v1);
}
