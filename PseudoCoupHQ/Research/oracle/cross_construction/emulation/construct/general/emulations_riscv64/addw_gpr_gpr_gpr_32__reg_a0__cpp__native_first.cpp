/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of addw_gpr_gpr_gpr_32__reg_a0__cpp__native_first.  The term's text, LITERAL:
   Concat(Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract */
#include <cstdint>

extern "C"
uint64_t
emu_addw_gpr_gpr_gpr_32__reg_a0__cpp__native_first(uint32_t a, uint32_t b)
{
    uint32_t v0 = (uint32_t)b;
    uint32_t v1 = (uint32_t)a;
    uint32_t v2 = (uint32_t)((uint32_t)(v1) + (uint32_t)(v0));
    uint32_t v3 = ((uint32_t)((uint32_t)(v2) >> 31) & UINT32_C(0x1));
    uint64_t v4 = (uint64_t)(((uint64_t)(v3) << 63) | ((uint64_t)(v3) << 62) | ((uint64_t)(v3) << 61) | ((uint64_t)(v3) << 60) | ((uint64_t)(v3) << 59) | ((uint64_t)(v3) << 58) | ((uint64_t)(v3) << 57) | ((uint64_t)(v3) << 56) | ((uint64_t)(v3) << 55) | ((uint64_t)(v3) << 54) | ((uint64_t)(v3) << 53) | ((uint64_t)(v3) << 52) | ((uint64_t)(v3) << 51) | ((uint64_t)(v3) << 50) | ((uint64_t)(v3) << 49) | ((uint64_t)(v3) << 48) | ((uint64_t)(v3) << 47) | ((uint64_t)(v3) << 46) | ((uint64_t)(v3) << 45) | ((uint64_t)(v3) << 44) | ((uint64_t)(v3) << 43) | ((uint64_t)(v3) << 42) | ((uint64_t)(v3) << 41) | ((uint64_t)(v3) << 40) | ((uint64_t)(v3) << 39) | ((uint64_t)(v3) << 38) | ((uint64_t)(v3) << 37) | ((uint64_t)(v3) << 36) | ((uint64_t)(v3) << 35) | ((uint64_t)(v3) << 34) | ((uint64_t)(v3) << 33) | ((uint64_t)(v3) << 32) | (uint64_t)(v2));
    return (uint64_t)(v4);
}
