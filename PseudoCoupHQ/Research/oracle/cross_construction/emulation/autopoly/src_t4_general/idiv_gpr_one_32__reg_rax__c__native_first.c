/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of idiv_gpr_one_32__reg_rax__c__native_first.  The term's text, LITERAL:
   Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2))))) */
#include <stdint.h>

uint64_t
emu_idiv_gpr_one_32__reg_rax__c__native_first(uint32_t a, uint32_t b, uint32_t c)
{
    uint32_t v0 = (uint32_t)c;
    uint32_t v1 = ((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1));
    uint64_t v2 = (uint64_t)(((uint64_t)(v1) << 63) | ((uint64_t)(v1) << 62) | ((uint64_t)(v1) << 61) | ((uint64_t)(v1) << 60) | ((uint64_t)(v1) << 59) | ((uint64_t)(v1) << 58) | ((uint64_t)(v1) << 57) | ((uint64_t)(v1) << 56) | ((uint64_t)(v1) << 55) | ((uint64_t)(v1) << 54) | ((uint64_t)(v1) << 53) | ((uint64_t)(v1) << 52) | ((uint64_t)(v1) << 51) | ((uint64_t)(v1) << 50) | ((uint64_t)(v1) << 49) | ((uint64_t)(v1) << 48) | ((uint64_t)(v1) << 47) | ((uint64_t)(v1) << 46) | ((uint64_t)(v1) << 45) | ((uint64_t)(v1) << 44) | ((uint64_t)(v1) << 43) | ((uint64_t)(v1) << 42) | ((uint64_t)(v1) << 41) | ((uint64_t)(v1) << 40) | ((uint64_t)(v1) << 39) | ((uint64_t)(v1) << 38) | ((uint64_t)(v1) << 37) | ((uint64_t)(v1) << 36) | ((uint64_t)(v1) << 35) | ((uint64_t)(v1) << 34) | ((uint64_t)(v1) << 33) | ((uint64_t)(v1) << 32) | (uint64_t)(v0));
    uint32_t v3 = (uint32_t)b;
    uint32_t v4 = (uint32_t)a;
    uint64_t v5 = (uint64_t)(((uint64_t)(v4) << 32) | (uint64_t)(v3));
    uint64_t v6 = (uint64_t)((int64_t)((int64_t)(v5)) / (int64_t)((int64_t)(v2)));
    uint32_t v7 = (uint32_t)((uint64_t)(v6) >> 0);
    uint64_t v8 = (uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)(v7));
    return (uint64_t)(v8);
}
