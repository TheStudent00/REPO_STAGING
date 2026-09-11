/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of div_gpr_one_64__reg_rdx__cpp__native_first.  The term's text, LITERAL:
   Extract(63, 0, bvurem_i(Concat(v0, v1), Concat(0, v2))) */
#include <cstdint>

extern "C"
uint64_t
emu_div_gpr_one_64__reg_rdx__cpp__native_first(uint64_t a, uint64_t b, uint64_t c)
{
    unsigned __int128 v0 = (unsigned __int128)(((unsigned __int128)(UINT64_C(0x0)) << 64) | (unsigned __int128)((uint64_t)c));
    unsigned __int128 v1 = (unsigned __int128)(((unsigned __int128)((uint64_t)a) << 64) | (unsigned __int128)((uint64_t)b));
    unsigned __int128 v2 = (unsigned __int128)((unsigned __int128)(v1) % (unsigned __int128)(v0));
    uint64_t v3 = (uint64_t)((unsigned __int128)(v2) >> 0);
    return (uint64_t)(v3);
}
