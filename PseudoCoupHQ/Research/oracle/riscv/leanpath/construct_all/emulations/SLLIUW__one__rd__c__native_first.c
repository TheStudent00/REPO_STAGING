/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of SLLIUW__one__rd__c__native_first.  The term's text, LITERAL:
    */
#include <stdint.h>

uint64_t
emu_SLLIUW__one__rd__c__native_first(uint32_t a, uint8_t b)
{
    uint32_t v0 = ((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x3f));
    uint64_t v1 = (uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(v0));
    uint32_t v2 = (uint32_t)a;
    uint64_t v3 = (uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)(v2));
    uint64_t v4 = (uint64_t)((uint64_t)(v3) << (unsigned)(uint64_t)(v1));
    return (uint64_t)(v4);
}
