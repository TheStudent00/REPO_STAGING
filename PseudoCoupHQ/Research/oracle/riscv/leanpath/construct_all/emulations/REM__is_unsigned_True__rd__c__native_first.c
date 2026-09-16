/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of REM__is_unsigned_True__rd__c__native_first.  The term's text, LITERAL:
    */
#include <stdint.h>

uint64_t
emu_REM__is_unsigned_True__rd__c__native_first(uint64_t a, uint64_t b)
{
    unsigned __int128 v0 = (unsigned __int128)(((unsigned __int128)(UINT64_C(0x0)) << 64) | (unsigned __int128)((uint64_t)a));
    unsigned __int128 v1 = (unsigned __int128)(((unsigned __int128)(UINT64_C(0x0)) << 64) | (unsigned __int128)((uint64_t)b));
    unsigned __int128 v2 = (unsigned __int128)((__int128)((__int128)(v1)) % (__int128)((__int128)(v0)));
    uint64_t v3 = (uint64_t)((unsigned __int128)(v2) >> 0);
    int v4 = (((uint64_t)((uint64_t)a) == (uint64_t)(UINT64_C(0x0)))) ? 1 : 0;
    uint64_t v5 = ((v4) ? (uint64_t)((uint64_t)b) : (uint64_t)(v3));
    return (uint64_t)(v5);
}
