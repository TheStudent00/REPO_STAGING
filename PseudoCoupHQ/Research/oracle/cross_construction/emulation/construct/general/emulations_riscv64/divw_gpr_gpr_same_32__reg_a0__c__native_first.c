/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of divw_gpr_gpr_same_32__reg_a0__c__native_first.  The term's text, LITERAL:
   Concat(If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Or(Extract */
#include <stdint.h>

uint64_t
emu_divw_gpr_gpr_same_32__reg_a0__c__native_first(uint32_t a)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = (uint32_t)((int32_t)((int32_t)(v0)) / (int32_t)((int32_t)(v0)));
    int v2 = (((uint32_t)(v0) == (uint32_t)(UINT32_C(0xffffffff)))) ? 1 : 0;
    int v3 = (((uint32_t)(v0) == (uint32_t)(UINT32_C(0x80000000)))) ? 1 : 0;
    int v4 = (((v3) && (v2))) ? 1 : 0;
    uint32_t v5 = ((v4) ? (uint32_t)(UINT32_C(0x80000000)) : (uint32_t)(v1));
    int v6 = (((uint32_t)(v0) == (uint32_t)(UINT32_C(0x0)))) ? 1 : 0;
    uint32_t v7 = ((v6) ? (uint32_t)(UINT32_C(0xffffffff)) : (uint32_t)(v5));
    uint32_t v8 = ((uint32_t)((uint32_t)(v1) >> 31) & UINT32_C(0x1));
    int v9 = (((v6) || (v4))) ? 1 : 0;
    uint32_t v10 = ((v9) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(v8));
    uint64_t v11 = (uint64_t)(((uint64_t)(v10) << 63) | ((uint64_t)(v10) << 62) | ((uint64_t)(v10) << 61) | ((uint64_t)(v10) << 60) | ((uint64_t)(v10) << 59) | ((uint64_t)(v10) << 58) | ((uint64_t)(v10) << 57) | ((uint64_t)(v10) << 56) | ((uint64_t)(v10) << 55) | ((uint64_t)(v10) << 54) | ((uint64_t)(v10) << 53) | ((uint64_t)(v10) << 52) | ((uint64_t)(v10) << 51) | ((uint64_t)(v10) << 50) | ((uint64_t)(v10) << 49) | ((uint64_t)(v10) << 48) | ((uint64_t)(v10) << 47) | ((uint64_t)(v10) << 46) | ((uint64_t)(v10) << 45) | ((uint64_t)(v10) << 44) | ((uint64_t)(v10) << 43) | ((uint64_t)(v10) << 42) | ((uint64_t)(v10) << 41) | ((uint64_t)(v10) << 40) | ((uint64_t)(v10) << 39) | ((uint64_t)(v10) << 38) | ((uint64_t)(v10) << 37) | ((uint64_t)(v10) << 36) | ((uint64_t)(v10) << 35) | ((uint64_t)(v10) << 34) | ((uint64_t)(v10) << 33) | ((uint64_t)(v10) << 32) | (uint64_t)(v7));
    return (uint64_t)(v11);
}
