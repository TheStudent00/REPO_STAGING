/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of seta_gpr_one_8__reg_rdi__cpp__native_first.  The term's text, LITERAL:
   Concat(Extract(63, 8, v2), If(And(ULE(Extract(7, 0, v0), Extract(7, 0, v1)), Not(Extract(7, 0, v0) == Extract(7, 0, v1))), 1, 0)) */
#include <cstdint>

extern "C"
uint64_t
emu_seta_gpr_one_8__reg_rdi__cpp__native_first(uint8_t a, uint8_t b, uint64_t c)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = (uint32_t)b;
    int v2 = (((uint32_t)(v1) == (uint32_t)(v0))) ? 1 : 0;
    int v3 = ((!(v2))) ? 1 : 0;
    int v4 = (((uint32_t)(v1) <= (uint32_t)(v0))) ? 1 : 0;
    int v5 = (((v4) && (v3))) ? 1 : 0;
    uint32_t v6 = ((v5) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0)));
    uint64_t v7 = ((uint64_t)((uint64_t)c >> 8) & UINT64_C(0xffffffffffffff));
    uint64_t v8 = (uint64_t)(((uint64_t)(v7) << 8) | (uint64_t)(v6));
    return (uint64_t)(v8);
}
