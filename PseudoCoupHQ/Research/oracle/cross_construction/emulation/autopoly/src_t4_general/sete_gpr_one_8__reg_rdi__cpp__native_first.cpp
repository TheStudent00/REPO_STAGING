/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of sete_gpr_one_8__reg_rdi__cpp__native_first.  The term's text, LITERAL:
   Concat(Extract(63, 8, v2), If(Extract(7, 0, v0) | Extract(7, 0, v1) == 0, 1, 0)) */
#include <cstdint>

extern "C"
uint64_t
emu_sete_gpr_one_8__reg_rdi__cpp__native_first(uint8_t a, uint8_t b, uint64_t c)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = (uint32_t)b;
    uint32_t v2 = ((uint32_t)((uint32_t)(v1) | (uint32_t)(v0)) & UINT32_C(0xff));
    int v3 = (((uint32_t)(v2) == (uint32_t)(UINT32_C(0x0)))) ? 1 : 0;
    uint32_t v4 = ((v3) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0)));
    uint64_t v5 = ((uint64_t)((uint64_t)c >> 8) & UINT64_C(0xffffffffffffff));
    uint64_t v6 = (uint64_t)(((uint64_t)(v5) << 8) | (uint64_t)(v4));
    return (uint64_t)(v6);
}
