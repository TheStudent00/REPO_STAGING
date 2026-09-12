/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of divuw_gpr_gpr_same_32__reg_a0__cpp__native_first.  The term's text, LITERAL:
   Concat(If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If */
#include <cstdint>

extern "C"
uint64_t
emu_divuw_gpr_gpr_same_32__reg_a0__cpp__native_first(uint32_t a)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = (uint32_t)((uint32_t)(v0) / (uint32_t)(v0));
    int v2 = (((uint32_t)(v0) == (uint32_t)(UINT32_C(0x0)))) ? 1 : 0;
    uint32_t v3 = ((v2) ? (uint32_t)(UINT32_C(0xffffffff)) : (uint32_t)(v1));
    uint32_t v4 = ((uint32_t)((uint32_t)(v1) >> 31) & UINT32_C(0x1));
    uint32_t v5 = ((v2) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(v4));
    uint64_t v6 = (uint64_t)(((uint64_t)(v5) << 63) | ((uint64_t)(v5) << 62) | ((uint64_t)(v5) << 61) | ((uint64_t)(v5) << 60) | ((uint64_t)(v5) << 59) | ((uint64_t)(v5) << 58) | ((uint64_t)(v5) << 57) | ((uint64_t)(v5) << 56) | ((uint64_t)(v5) << 55) | ((uint64_t)(v5) << 54) | ((uint64_t)(v5) << 53) | ((uint64_t)(v5) << 52) | ((uint64_t)(v5) << 51) | ((uint64_t)(v5) << 50) | ((uint64_t)(v5) << 49) | ((uint64_t)(v5) << 48) | ((uint64_t)(v5) << 47) | ((uint64_t)(v5) << 46) | ((uint64_t)(v5) << 45) | ((uint64_t)(v5) << 44) | ((uint64_t)(v5) << 43) | ((uint64_t)(v5) << 42) | ((uint64_t)(v5) << 41) | ((uint64_t)(v5) << 40) | ((uint64_t)(v5) << 39) | ((uint64_t)(v5) << 38) | ((uint64_t)(v5) << 37) | ((uint64_t)(v5) << 36) | ((uint64_t)(v5) << 35) | ((uint64_t)(v5) << 34) | ((uint64_t)(v5) << 33) | ((uint64_t)(v5) << 32) | (uint64_t)(v3));
    return (uint64_t)(v6);
}
