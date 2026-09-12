/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of mulhu_gpr_gpr_same_64__reg_a0__cpp__native_first.  The term's text, LITERAL:
   Extract(127, 64, Concat(0, v0)*Concat(0, v0)) */
#include <cstdint>

extern "C"
uint64_t
emu_mulhu_gpr_gpr_same_64__reg_a0__cpp__native_first(uint64_t a)
{
    unsigned __int128 v0 = (unsigned __int128)(((unsigned __int128)(UINT64_C(0x0)) << 64) | (unsigned __int128)((uint64_t)a));
    unsigned __int128 v1 = (unsigned __int128)((unsigned __int128)(v0) * (unsigned __int128)(v0));
    uint64_t v2 = (uint64_t)((unsigned __int128)(v1) >> 64);
    return (uint64_t)(v2);
}
