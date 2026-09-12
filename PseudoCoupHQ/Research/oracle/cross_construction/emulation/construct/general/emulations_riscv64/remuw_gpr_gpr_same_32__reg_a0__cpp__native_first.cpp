/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of remuw_gpr_gpr_same_32__reg_a0__cpp__native_first.  The term's text, LITERAL:
   Concat(If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), Extract(31, 31, bvurem_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), Extract(31, 31, bvurem_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), Extract(31, 31, bvurem_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), Extract(31, 31, bvurem_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), Extract(31, 31, bvurem_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), Extract(31, 31, bvurem_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), Extract(31, 31, bvurem_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), Extract(31, 31, bvurem_i( */
#include <cstdint>

extern "C"
uint64_t
emu_remuw_gpr_gpr_same_32__reg_a0__cpp__native_first(uint32_t a)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = (uint32_t)((uint32_t)(v0) % (uint32_t)(v0));
    int v2 = (((uint32_t)(v0) == (uint32_t)(UINT32_C(0x0)))) ? 1 : 0;
    uint32_t v3 = ((v2) ? (uint32_t)(v0) : (uint32_t)(v1));
    uint32_t v4 = ((uint32_t)((uint32_t)(v1) >> 31) & UINT32_C(0x1));
    uint32_t v5 = ((uint32_t)((uint32_t)a >> 31) & UINT32_C(0x1));
    uint32_t v6 = ((v2) ? (uint32_t)(v5) : (uint32_t)(v4));
    uint64_t v7 = (uint64_t)(((uint64_t)(v6) << 63) | ((uint64_t)(v6) << 62) | ((uint64_t)(v6) << 61) | ((uint64_t)(v6) << 60) | ((uint64_t)(v6) << 59) | ((uint64_t)(v6) << 58) | ((uint64_t)(v6) << 57) | ((uint64_t)(v6) << 56) | ((uint64_t)(v6) << 55) | ((uint64_t)(v6) << 54) | ((uint64_t)(v6) << 53) | ((uint64_t)(v6) << 52) | ((uint64_t)(v6) << 51) | ((uint64_t)(v6) << 50) | ((uint64_t)(v6) << 49) | ((uint64_t)(v6) << 48) | ((uint64_t)(v6) << 47) | ((uint64_t)(v6) << 46) | ((uint64_t)(v6) << 45) | ((uint64_t)(v6) << 44) | ((uint64_t)(v6) << 43) | ((uint64_t)(v6) << 42) | ((uint64_t)(v6) << 41) | ((uint64_t)(v6) << 40) | ((uint64_t)(v6) << 39) | ((uint64_t)(v6) << 38) | ((uint64_t)(v6) << 37) | ((uint64_t)(v6) << 36) | ((uint64_t)(v6) << 35) | ((uint64_t)(v6) << 34) | ((uint64_t)(v6) << 33) | ((uint64_t)(v6) << 32) | (uint64_t)(v3));
    return (uint64_t)(v7);
}
