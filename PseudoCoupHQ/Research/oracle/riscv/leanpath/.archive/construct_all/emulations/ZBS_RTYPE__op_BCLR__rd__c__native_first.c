/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of ZBS_RTYPE__op_BCLR__rd__c__native_first.  The term's text, LITERAL:
    */
#include <stdint.h>

uint64_t
emu_ZBS_RTYPE__op_BCLR__rd__c__native_first(uint8_t a, uint64_t b)
{
    uint32_t v0 = ((uint32_t)((uint32_t)a >> 0) & UINT32_C(0x3f));
    uint64_t v1 = (uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(v0));
    uint64_t v2 = (uint64_t)((uint64_t)(UINT64_C(0x1)) << (unsigned)(uint64_t)(v1));
    uint64_t v3 = (uint64_t)(~(uint64_t)((uint64_t)b));
    uint64_t v4 = (uint64_t)((uint64_t)(v3) | (uint64_t)(v2));
    uint64_t v5 = (uint64_t)(~(uint64_t)(v4));
    return (uint64_t)(v5);
}
