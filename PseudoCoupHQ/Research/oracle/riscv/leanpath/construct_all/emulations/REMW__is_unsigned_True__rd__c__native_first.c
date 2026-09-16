/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of REMW__is_unsigned_True__rd__c__native_first.  The term's text, LITERAL:
    */
#include <stdint.h>

uint64_t
emu_REMW__is_unsigned_True__rd__c__native_first(uint32_t a, uint32_t b)
{
    uint32_t v0 = (uint32_t)a;
    unsigned __int128 v1 = (unsigned __int128)(((unsigned __int128)((((unsigned __int128)UINT64_C(0x0) << 64) | (unsigned __int128)UINT64_C(0x0))) << 32) | (unsigned __int128)(v0));
    uint32_t v2 = (uint32_t)b;
    unsigned __int128 v3 = (unsigned __int128)(((unsigned __int128)((((unsigned __int128)UINT64_C(0x0) << 64) | (unsigned __int128)UINT64_C(0x0))) << 32) | (unsigned __int128)(v2));
    unsigned __int128 v4 = (unsigned __int128)((__int128)((__int128)(v3)) % (__int128)((__int128)(v1)));
    uint32_t v5 = (uint32_t)((unsigned __int128)(v4) >> 0);
    int v6 = (((uint32_t)(v0) == (uint32_t)(UINT32_C(0x0)))) ? 1 : 0;
    uint32_t v7 = ((v6) ? (uint32_t)(v2) : (uint32_t)(v5));
    uint32_t v8 = ((uint32_t)((unsigned __int128)(v4) >> 31) & UINT32_C(0x1));
    uint32_t v9 = ((uint32_t)((uint32_t)b >> 31) & UINT32_C(0x1));
    uint32_t v10 = ((v6) ? (uint32_t)(v9) : (uint32_t)(v8));
    uint64_t v11 = (uint64_t)(((uint64_t)(v10) << 63) | ((uint64_t)(v10) << 62) | ((uint64_t)(v10) << 61) | ((uint64_t)(v10) << 60) | ((uint64_t)(v10) << 59) | ((uint64_t)(v10) << 58) | ((uint64_t)(v10) << 57) | ((uint64_t)(v10) << 56) | ((uint64_t)(v10) << 55) | ((uint64_t)(v10) << 54) | ((uint64_t)(v10) << 53) | ((uint64_t)(v10) << 52) | ((uint64_t)(v10) << 51) | ((uint64_t)(v10) << 50) | ((uint64_t)(v10) << 49) | ((uint64_t)(v10) << 48) | ((uint64_t)(v10) << 47) | ((uint64_t)(v10) << 46) | ((uint64_t)(v10) << 45) | ((uint64_t)(v10) << 44) | ((uint64_t)(v10) << 43) | ((uint64_t)(v10) << 42) | ((uint64_t)(v10) << 41) | ((uint64_t)(v10) << 40) | ((uint64_t)(v10) << 39) | ((uint64_t)(v10) << 38) | ((uint64_t)(v10) << 37) | ((uint64_t)(v10) << 36) | ((uint64_t)(v10) << 35) | ((uint64_t)(v10) << 34) | ((uint64_t)(v10) << 33) | ((uint64_t)(v10) << 32) | (uint64_t)(v7));
    return (uint64_t)(v11);
}
