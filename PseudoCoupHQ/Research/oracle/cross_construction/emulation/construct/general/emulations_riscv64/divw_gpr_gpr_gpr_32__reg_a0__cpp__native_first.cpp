/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of divw_gpr_gpr_gpr_32__reg_a0__cpp__native_first.  The term's text, LITERAL:
   Concat(If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v1) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v1) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v1) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v1) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v1) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Or(Extract */
#include <cstdint>

extern "C"
uint64_t
emu_divw_gpr_gpr_gpr_32__reg_a0__cpp__native_first(uint32_t a, uint32_t b)
{
    uint32_t v0 = (uint32_t)b;
    uint32_t v1 = (uint32_t)a;
    uint32_t v2 = (uint32_t)((int32_t)((int32_t)(v1)) / (int32_t)((int32_t)(v0)));
    int v3 = (((uint32_t)(v0) == (uint32_t)(UINT32_C(0xffffffff)))) ? 1 : 0;
    int v4 = (((uint32_t)(v1) == (uint32_t)(UINT32_C(0x80000000)))) ? 1 : 0;
    int v5 = (((v4) && (v3))) ? 1 : 0;
    uint32_t v6 = ((v5) ? (uint32_t)(UINT32_C(0x80000000)) : (uint32_t)(v2));
    int v7 = (((uint32_t)(v0) == (uint32_t)(UINT32_C(0x0)))) ? 1 : 0;
    uint32_t v8 = ((v7) ? (uint32_t)(UINT32_C(0xffffffff)) : (uint32_t)(v6));
    uint32_t v9 = ((uint32_t)((uint32_t)(v2) >> 31) & UINT32_C(0x1));
    int v10 = (((v7) || (v5))) ? 1 : 0;
    uint32_t v11 = ((v10) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(v9));
    uint64_t v12 = (uint64_t)(((uint64_t)(v11) << 63) | ((uint64_t)(v11) << 62) | ((uint64_t)(v11) << 61) | ((uint64_t)(v11) << 60) | ((uint64_t)(v11) << 59) | ((uint64_t)(v11) << 58) | ((uint64_t)(v11) << 57) | ((uint64_t)(v11) << 56) | ((uint64_t)(v11) << 55) | ((uint64_t)(v11) << 54) | ((uint64_t)(v11) << 53) | ((uint64_t)(v11) << 52) | ((uint64_t)(v11) << 51) | ((uint64_t)(v11) << 50) | ((uint64_t)(v11) << 49) | ((uint64_t)(v11) << 48) | ((uint64_t)(v11) << 47) | ((uint64_t)(v11) << 46) | ((uint64_t)(v11) << 45) | ((uint64_t)(v11) << 44) | ((uint64_t)(v11) << 43) | ((uint64_t)(v11) << 42) | ((uint64_t)(v11) << 41) | ((uint64_t)(v11) << 40) | ((uint64_t)(v11) << 39) | ((uint64_t)(v11) << 38) | ((uint64_t)(v11) << 37) | ((uint64_t)(v11) << 36) | ((uint64_t)(v11) << 35) | ((uint64_t)(v11) << 34) | ((uint64_t)(v11) << 33) | ((uint64_t)(v11) << 32) | (uint64_t)(v8));
    return (uint64_t)(v12);
}
