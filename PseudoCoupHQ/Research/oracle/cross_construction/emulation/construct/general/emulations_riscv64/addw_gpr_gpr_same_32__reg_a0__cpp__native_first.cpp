/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of addw_gpr_gpr_same_32__reg_a0__cpp__native_first.  The term's text, LITERAL:
   Concat(Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)*2), Extract(31, 31, Extract(31, 0, v0)* */
#include <cstdint>

extern "C"
uint64_t
emu_addw_gpr_gpr_same_32__reg_a0__cpp__native_first(uint32_t a)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = (uint32_t)((uint32_t)(v0) * (uint32_t)(UINT32_C(0x2)));
    uint32_t v2 = ((uint32_t)((uint32_t)(v1) >> 31) & UINT32_C(0x1));
    uint64_t v3 = (uint64_t)(((uint64_t)(v2) << 63) | ((uint64_t)(v2) << 62) | ((uint64_t)(v2) << 61) | ((uint64_t)(v2) << 60) | ((uint64_t)(v2) << 59) | ((uint64_t)(v2) << 58) | ((uint64_t)(v2) << 57) | ((uint64_t)(v2) << 56) | ((uint64_t)(v2) << 55) | ((uint64_t)(v2) << 54) | ((uint64_t)(v2) << 53) | ((uint64_t)(v2) << 52) | ((uint64_t)(v2) << 51) | ((uint64_t)(v2) << 50) | ((uint64_t)(v2) << 49) | ((uint64_t)(v2) << 48) | ((uint64_t)(v2) << 47) | ((uint64_t)(v2) << 46) | ((uint64_t)(v2) << 45) | ((uint64_t)(v2) << 44) | ((uint64_t)(v2) << 43) | ((uint64_t)(v2) << 42) | ((uint64_t)(v2) << 41) | ((uint64_t)(v2) << 40) | ((uint64_t)(v2) << 39) | ((uint64_t)(v2) << 38) | ((uint64_t)(v2) << 37) | ((uint64_t)(v2) << 36) | ((uint64_t)(v2) << 35) | ((uint64_t)(v2) << 34) | ((uint64_t)(v2) << 33) | ((uint64_t)(v2) << 32) | (uint64_t)(v1));
    return (uint64_t)(v3);
}
