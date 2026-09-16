/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of ADDIW__one__rd__c__native_first.  The term's text, LITERAL:
    */
#include <stdint.h>

uint64_t
emu_ADDIW__one__rd__c__native_first(uint32_t a, uint16_t b)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = ((uint32_t)((uint32_t)b >> 0) & UINT32_C(0xfff));
    uint32_t v2 = ((uint32_t)((uint32_t)b >> 11) & UINT32_C(0x1));
    uint32_t v3 = (uint32_t)(((uint32_t)(v2) << 31) | ((uint32_t)(v2) << 30) | ((uint32_t)(v2) << 29) | ((uint32_t)(v2) << 28) | ((uint32_t)(v2) << 27) | ((uint32_t)(v2) << 26) | ((uint32_t)(v2) << 25) | ((uint32_t)(v2) << 24) | ((uint32_t)(v2) << 23) | ((uint32_t)(v2) << 22) | ((uint32_t)(v2) << 21) | ((uint32_t)(v2) << 20) | ((uint32_t)(v2) << 19) | ((uint32_t)(v2) << 18) | ((uint32_t)(v2) << 17) | ((uint32_t)(v2) << 16) | ((uint32_t)(v2) << 15) | ((uint32_t)(v2) << 14) | ((uint32_t)(v2) << 13) | ((uint32_t)(v2) << 12) | (uint32_t)(v1));
    uint32_t v4 = (uint32_t)((uint32_t)(v3) + (uint32_t)(v0));
    uint32_t v5 = ((uint32_t)((uint32_t)(v4) >> 31) & UINT32_C(0x1));
    uint64_t v6 = (uint64_t)(((uint64_t)(v5) << 63) | ((uint64_t)(v5) << 62) | ((uint64_t)(v5) << 61) | ((uint64_t)(v5) << 60) | ((uint64_t)(v5) << 59) | ((uint64_t)(v5) << 58) | ((uint64_t)(v5) << 57) | ((uint64_t)(v5) << 56) | ((uint64_t)(v5) << 55) | ((uint64_t)(v5) << 54) | ((uint64_t)(v5) << 53) | ((uint64_t)(v5) << 52) | ((uint64_t)(v5) << 51) | ((uint64_t)(v5) << 50) | ((uint64_t)(v5) << 49) | ((uint64_t)(v5) << 48) | ((uint64_t)(v5) << 47) | ((uint64_t)(v5) << 46) | ((uint64_t)(v5) << 45) | ((uint64_t)(v5) << 44) | ((uint64_t)(v5) << 43) | ((uint64_t)(v5) << 42) | ((uint64_t)(v5) << 41) | ((uint64_t)(v5) << 40) | ((uint64_t)(v5) << 39) | ((uint64_t)(v5) << 38) | ((uint64_t)(v5) << 37) | ((uint64_t)(v5) << 36) | ((uint64_t)(v5) << 35) | ((uint64_t)(v5) << 34) | ((uint64_t)(v5) << 33) | ((uint64_t)(v5) << 32) | (uint64_t)(v4));
    return (uint64_t)(v6);
}
