/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of flw_fpr_fpr_32__freg_fa0__c__all_constructed.  The term's text, LITERAL:
   Concat(4294967295, Extract(31, 0, v0)) */
#include <stdint.h>

uint64_t
emu_flw_fpr_fpr_32__freg_fa0__c__all_constructed(uint32_t a)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = v0;
    uint32_t v2 = UINT32_C(0xffffffff);
    uint64_t v3 = (uint64_t)(((uint64_t)(v2) << 32) | (uint64_t)(v1));
    return (uint64_t)(v3);
}
