/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of bne_gpr_gpr_same_64__branch_condition__c__native_first.  The term's text, LITERAL:
   If(v0 == v1, 0, 1) */
#include <stdint.h>

uint64_t
emu_bne_gpr_gpr_same_64__branch_condition__c__native_first(uint64_t a, uint64_t b)
{
    int v0 = (((uint64_t)((uint64_t)a) == (uint64_t)((uint64_t)b))) ? 1 : 0;
    uint64_t v1 = ((v0) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)(UINT64_C(0x1)));
    return (uint64_t)(v1);
}
