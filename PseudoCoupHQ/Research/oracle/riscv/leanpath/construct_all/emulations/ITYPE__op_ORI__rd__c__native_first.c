/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of ITYPE__op_ORI__rd__c__native_first.  The term's text, LITERAL:
    */
#include <stdint.h>

uint64_t
emu_ITYPE__op_ORI__rd__c__native_first(uint64_t a, uint16_t b)
{
    uint64_t v0 = ((uint64_t)((uint64_t)a >> 0) & UINT64_C(0x3fffffffffffffff));
    uint32_t v1 = ((uint32_t)((uint32_t)b >> 0) & UINT32_C(0xfff));
    uint32_t v2 = ((uint32_t)((uint32_t)b >> 11) & UINT32_C(0x1));
    uint64_t v3 = ((uint64_t)(((uint64_t)(v2) << 61) | ((uint64_t)(v2) << 60) | ((uint64_t)(v2) << 59) | ((uint64_t)(v2) << 58) | ((uint64_t)(v2) << 57) | ((uint64_t)(v2) << 56) | ((uint64_t)(v2) << 55) | ((uint64_t)(v2) << 54) | ((uint64_t)(v2) << 53) | ((uint64_t)(v2) << 52) | ((uint64_t)(v2) << 51) | ((uint64_t)(v2) << 50) | ((uint64_t)(v2) << 49) | ((uint64_t)(v2) << 48) | ((uint64_t)(v2) << 47) | ((uint64_t)(v2) << 46) | ((uint64_t)(v2) << 45) | ((uint64_t)(v2) << 44) | ((uint64_t)(v2) << 43) | ((uint64_t)(v2) << 42) | ((uint64_t)(v2) << 41) | ((uint64_t)(v2) << 40) | ((uint64_t)(v2) << 39) | ((uint64_t)(v2) << 38) | ((uint64_t)(v2) << 37) | ((uint64_t)(v2) << 36) | ((uint64_t)(v2) << 35) | ((uint64_t)(v2) << 34) | ((uint64_t)(v2) << 33) | ((uint64_t)(v2) << 32) | ((uint64_t)(v2) << 31) | ((uint64_t)(v2) << 30) | ((uint64_t)(v2) << 29) | ((uint64_t)(v2) << 28) | ((uint64_t)(v2) << 27) | ((uint64_t)(v2) << 26) | ((uint64_t)(v2) << 25) | ((uint64_t)(v2) << 24) | ((uint64_t)(v2) << 23) | ((uint64_t)(v2) << 22) | ((uint64_t)(v2) << 21) | ((uint64_t)(v2) << 20) | ((uint64_t)(v2) << 19) | ((uint64_t)(v2) << 18) | ((uint64_t)(v2) << 17) | ((uint64_t)(v2) << 16) | ((uint64_t)(v2) << 15) | ((uint64_t)(v2) << 14) | ((uint64_t)(v2) << 13) | ((uint64_t)(v2) << 12) | (uint64_t)(v1)) & UINT64_C(0x3fffffffffffffff));
    uint64_t v4 = ((uint64_t)((uint64_t)(v3) | (uint64_t)(v0)) & UINT64_C(0x3fffffffffffffff));
    uint32_t v5 = ((uint32_t)((uint64_t)a >> 62) & UINT32_C(0x1));
    uint32_t v6 = ((uint32_t)((uint32_t)(v2) | (uint32_t)(v5)) & UINT32_C(0x1));
    uint32_t v7 = ((uint32_t)((uint64_t)a >> 63) & UINT32_C(0x1));
    uint32_t v8 = ((uint32_t)((uint32_t)(v2) | (uint32_t)(v7)) & UINT32_C(0x1));
    uint64_t v9 = (uint64_t)(((uint64_t)(v8) << 63) | ((uint64_t)(v6) << 62) | (uint64_t)(v4));
    return (uint64_t)(v9);
}
