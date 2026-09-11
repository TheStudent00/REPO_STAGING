/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of or_gpr_gpr_32__flags__c__native_first.  The term's text, LITERAL:
   Concat(Extract(31, 0, v0) | Extract(31, 0, v1), 0) */
#include <stdint.h>

uint64_t
emu_or_gpr_gpr_32__flags__c__native_first(uint32_t a, uint32_t b)
{
    uint32_t v0 = (uint32_t)b;
    uint32_t v1 = (uint32_t)a;
    uint32_t v2 = (uint32_t)((uint32_t)(v1) | (uint32_t)(v0));
    uint64_t v3 = (uint64_t)(((uint64_t)(v2) << 32) | (uint64_t)(UINT32_C(0x0)));
    return (uint64_t)(v3);
}
