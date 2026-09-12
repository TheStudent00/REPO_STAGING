/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of czero_eqz_gpr_gpr_same_64__reg_a0__cpp__native_first.  The term's text, LITERAL:
   If(v0 == 0, 0, v0) */
#include <cstdint>

extern "C"
uint64_t
emu_czero_eqz_gpr_gpr_same_64__reg_a0__cpp__native_first(uint64_t a)
{
    int v0 = (((uint64_t)((uint64_t)a) == (uint64_t)(UINT64_C(0x0)))) ? 1 : 0;
    uint64_t v1 = ((v0) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)((uint64_t)a));
    return (uint64_t)(v1);
}
