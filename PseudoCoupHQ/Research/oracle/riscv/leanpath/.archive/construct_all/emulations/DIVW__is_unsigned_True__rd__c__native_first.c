/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of DIVW__is_unsigned_True__rd__c__native_first.  The term's text, LITERAL:
    */
#include <stdint.h>

uint64_t
emu_DIVW__is_unsigned_True__rd__c__native_first(uint32_t a, uint32_t b)
{
    uint32_t v0 = (uint32_t)a;
    unsigned __int128 v1 = (unsigned __int128)(((unsigned __int128)((((unsigned __int128)UINT64_C(0x0) << 64) | (unsigned __int128)UINT64_C(0x0))) << 32) | (unsigned __int128)(v0));
    uint32_t v2 = (uint32_t)b;
    unsigned __int128 v3 = (unsigned __int128)(((unsigned __int128)((((unsigned __int128)UINT64_C(0x0) << 64) | (unsigned __int128)UINT64_C(0x0))) << 32) | (unsigned __int128)(v2));
    unsigned __int128 v4 = (unsigned __int128)((__int128)((__int128)(v3)) / (__int128)((__int128)(v1)));
    uint32_t v5 = (uint32_t)((unsigned __int128)(v4) >> 0);
    int v6 = (((uint32_t)(v0) == (uint32_t)(UINT32_C(0x0)))) ? 1 : 0;
    uint32_t v7 = ((v6) ? (uint32_t)(UINT32_C(0xffffffff)) : (uint32_t)(v5));
    uint32_t v8 = ((uint32_t)((unsigned __int128)(v4) >> 31) & UINT32_C(0x1));
    uint32_t v9 = ((v6) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(v8));
    uint64_t v10 = (uint64_t)(((uint64_t)(v9) << 63) | ((uint64_t)(v9) << 62) | ((uint64_t)(v9) << 61) | ((uint64_t)(v9) << 60) | ((uint64_t)(v9) << 59) | ((uint64_t)(v9) << 58) | ((uint64_t)(v9) << 57) | ((uint64_t)(v9) << 56) | ((uint64_t)(v9) << 55) | ((uint64_t)(v9) << 54) | ((uint64_t)(v9) << 53) | ((uint64_t)(v9) << 52) | ((uint64_t)(v9) << 51) | ((uint64_t)(v9) << 50) | ((uint64_t)(v9) << 49) | ((uint64_t)(v9) << 48) | ((uint64_t)(v9) << 47) | ((uint64_t)(v9) << 46) | ((uint64_t)(v9) << 45) | ((uint64_t)(v9) << 44) | ((uint64_t)(v9) << 43) | ((uint64_t)(v9) << 42) | ((uint64_t)(v9) << 41) | ((uint64_t)(v9) << 40) | ((uint64_t)(v9) << 39) | ((uint64_t)(v9) << 38) | ((uint64_t)(v9) << 37) | ((uint64_t)(v9) << 36) | ((uint64_t)(v9) << 35) | ((uint64_t)(v9) << 34) | ((uint64_t)(v9) << 33) | ((uint64_t)(v9) << 32) | (uint64_t)(v7));
    return (uint64_t)(v10);
}
