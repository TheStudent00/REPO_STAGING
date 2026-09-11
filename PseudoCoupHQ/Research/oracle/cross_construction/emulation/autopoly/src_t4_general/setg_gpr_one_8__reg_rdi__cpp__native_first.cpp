/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of setg_gpr_one_8__reg_rdi__cpp__native_first.  The term's text, LITERAL:
   Concat(Extract(63, 8, v2), If(And(Not(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) == 0), Or(Extract(7, 7, v0) == 0, Extract(7, 7, v1) == 0)), 1, 0)) */
#include <cstdint>

extern "C"
uint64_t
emu_setg_gpr_one_8__reg_rdi__cpp__native_first(uint8_t a, uint8_t b, uint64_t c)
{
    uint32_t v0 = ((uint32_t)((uint32_t)a >> 7) & UINT32_C(0x1));
    int v1 = (((uint32_t)(v0) == (uint32_t)(UINT32_C(0x0)))) ? 1 : 0;
    uint32_t v2 = ((uint32_t)((uint32_t)b >> 7) & UINT32_C(0x1));
    int v3 = (((uint32_t)(v2) == (uint32_t)(UINT32_C(0x0)))) ? 1 : 0;
    int v4 = (((v3) || (v1))) ? 1 : 0;
    uint32_t v5 = (uint32_t)a;
    uint32_t v6 = ((uint32_t)(~(uint32_t)(v5)) & UINT32_C(0xff));
    uint32_t v7 = (uint32_t)b;
    uint32_t v8 = ((uint32_t)(~(uint32_t)(v7)) & UINT32_C(0xff));
    uint32_t v9 = ((uint32_t)((uint32_t)(v8) | (uint32_t)(v6)) & UINT32_C(0xff));
    uint32_t v10 = ((uint32_t)(~(uint32_t)(v9)) & UINT32_C(0xff));
    int v11 = (((uint32_t)(v10) == (uint32_t)(UINT32_C(0x0)))) ? 1 : 0;
    int v12 = ((!(v11))) ? 1 : 0;
    int v13 = (((v12) && (v4))) ? 1 : 0;
    uint32_t v14 = ((v13) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0)));
    uint64_t v15 = ((uint64_t)((uint64_t)c >> 8) & UINT64_C(0xffffffffffffff));
    uint64_t v16 = (uint64_t)(((uint64_t)(v15) << 8) | (uint64_t)(v14));
    return (uint64_t)(v16);
}
