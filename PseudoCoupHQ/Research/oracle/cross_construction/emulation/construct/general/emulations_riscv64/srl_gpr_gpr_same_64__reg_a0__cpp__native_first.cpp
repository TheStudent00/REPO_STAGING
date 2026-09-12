/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of srl_gpr_gpr_same_64__reg_a0__cpp__native_first.  The term's text, LITERAL:
   LShR(v0, Concat(0, Extract(5, 0, v0))) */
#include <cstdint>

extern "C"
uint64_t
emu_srl_gpr_gpr_same_64__reg_a0__cpp__native_first(uint64_t a)
{
    uint32_t v0 = ((uint32_t)((uint64_t)a >> 0) & UINT32_C(0x3f));
    uint64_t v1 = (uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(v0));
    uint64_t v2 = (uint64_t)((uint64_t)((uint64_t)a) >> (unsigned)(uint64_t)(v1));
    return (uint64_t)(v2);
}
