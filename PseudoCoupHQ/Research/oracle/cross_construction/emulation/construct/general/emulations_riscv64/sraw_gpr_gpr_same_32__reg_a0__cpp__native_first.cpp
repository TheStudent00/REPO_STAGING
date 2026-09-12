/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of sraw_gpr_gpr_same_32__reg_a0__cpp__native_first.  The term's text, LITERAL:
   Concat(Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v0))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v0))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v0))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v0))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v0))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v0))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v0))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v0))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v0))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v0))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v0))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v0))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v0) */
#include <cstdint>

extern "C"
uint64_t
emu_sraw_gpr_gpr_same_32__reg_a0__cpp__native_first(uint32_t a)
{
    uint32_t v0 = ((uint32_t)((uint32_t)a >> 0) & UINT32_C(0x1f));
    uint32_t v1 = (uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(v0));
    uint32_t v2 = (uint32_t)a;
    uint32_t v3 = (uint32_t)((int32_t)(v2) >> (unsigned)(uint32_t)(v1));
    uint32_t v4 = ((uint32_t)((uint32_t)(v3) >> 31) & UINT32_C(0x1));
    uint64_t v5 = (uint64_t)(((uint64_t)(v4) << 63) | ((uint64_t)(v4) << 62) | ((uint64_t)(v4) << 61) | ((uint64_t)(v4) << 60) | ((uint64_t)(v4) << 59) | ((uint64_t)(v4) << 58) | ((uint64_t)(v4) << 57) | ((uint64_t)(v4) << 56) | ((uint64_t)(v4) << 55) | ((uint64_t)(v4) << 54) | ((uint64_t)(v4) << 53) | ((uint64_t)(v4) << 52) | ((uint64_t)(v4) << 51) | ((uint64_t)(v4) << 50) | ((uint64_t)(v4) << 49) | ((uint64_t)(v4) << 48) | ((uint64_t)(v4) << 47) | ((uint64_t)(v4) << 46) | ((uint64_t)(v4) << 45) | ((uint64_t)(v4) << 44) | ((uint64_t)(v4) << 43) | ((uint64_t)(v4) << 42) | ((uint64_t)(v4) << 41) | ((uint64_t)(v4) << 40) | ((uint64_t)(v4) << 39) | ((uint64_t)(v4) << 38) | ((uint64_t)(v4) << 37) | ((uint64_t)(v4) << 36) | ((uint64_t)(v4) << 35) | ((uint64_t)(v4) << 34) | ((uint64_t)(v4) << 33) | ((uint64_t)(v4) << 32) | (uint64_t)(v3));
    return (uint64_t)(v5);
}
