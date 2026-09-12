/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of remu_gpr_gpr_gpr_64__reg_a0__cpp__native_first.  The term's text, LITERAL:
   If(v0 == 0, v1, bvurem_i(v1, v0)) */
#include <cstdint>

extern "C"
uint64_t
emu_remu_gpr_gpr_gpr_64__reg_a0__cpp__native_first(uint64_t a, uint64_t b)
{
    uint64_t v0 = (uint64_t)((uint64_t)((uint64_t)b) % (uint64_t)((uint64_t)a));
    int v1 = (((uint64_t)((uint64_t)a) == (uint64_t)(UINT64_C(0x0)))) ? 1 : 0;
    uint64_t v2 = ((v1) ? (uint64_t)((uint64_t)b) : (uint64_t)(v0));
    return (uint64_t)(v2);
}
