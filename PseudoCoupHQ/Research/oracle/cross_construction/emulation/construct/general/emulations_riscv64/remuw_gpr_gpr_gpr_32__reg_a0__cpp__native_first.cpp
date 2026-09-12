/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of remuw_gpr_gpr_gpr_32__reg_a0__cpp__native_first.  The term's text, LITERAL:
   Concat(If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i( */
#include <cstdint>

extern "C"
uint64_t
emu_remuw_gpr_gpr_gpr_32__reg_a0__cpp__native_first(uint32_t a, uint32_t b)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = (uint32_t)b;
    uint32_t v2 = (uint32_t)((uint32_t)(v1) % (uint32_t)(v0));
    int v3 = (((uint32_t)(v0) == (uint32_t)(UINT32_C(0x0)))) ? 1 : 0;
    uint32_t v4 = ((v3) ? (uint32_t)(v1) : (uint32_t)(v2));
    uint32_t v5 = ((uint32_t)((uint32_t)(v2) >> 31) & UINT32_C(0x1));
    uint32_t v6 = ((uint32_t)((uint32_t)b >> 31) & UINT32_C(0x1));
    uint32_t v7 = ((v3) ? (uint32_t)(v6) : (uint32_t)(v5));
    uint64_t v8 = (uint64_t)(((uint64_t)(v7) << 63) | ((uint64_t)(v7) << 62) | ((uint64_t)(v7) << 61) | ((uint64_t)(v7) << 60) | ((uint64_t)(v7) << 59) | ((uint64_t)(v7) << 58) | ((uint64_t)(v7) << 57) | ((uint64_t)(v7) << 56) | ((uint64_t)(v7) << 55) | ((uint64_t)(v7) << 54) | ((uint64_t)(v7) << 53) | ((uint64_t)(v7) << 52) | ((uint64_t)(v7) << 51) | ((uint64_t)(v7) << 50) | ((uint64_t)(v7) << 49) | ((uint64_t)(v7) << 48) | ((uint64_t)(v7) << 47) | ((uint64_t)(v7) << 46) | ((uint64_t)(v7) << 45) | ((uint64_t)(v7) << 44) | ((uint64_t)(v7) << 43) | ((uint64_t)(v7) << 42) | ((uint64_t)(v7) << 41) | ((uint64_t)(v7) << 40) | ((uint64_t)(v7) << 39) | ((uint64_t)(v7) << 38) | ((uint64_t)(v7) << 37) | ((uint64_t)(v7) << 36) | ((uint64_t)(v7) << 35) | ((uint64_t)(v7) << 34) | ((uint64_t)(v7) << 33) | ((uint64_t)(v7) << 32) | (uint64_t)(v4));
    return (uint64_t)(v8);
}
