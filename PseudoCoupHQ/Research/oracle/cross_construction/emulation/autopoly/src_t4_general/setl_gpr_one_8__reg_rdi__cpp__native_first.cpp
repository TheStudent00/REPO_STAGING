/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of setl_gpr_one_8__reg_rdi__cpp__native_first.  The term's text, LITERAL:
   Concat(Extract(63, 8, v2), If(Extract(7, 7, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(7, 7, Concat(Extract(7, 7, v0), Extract(7, 0, v0))*511 + Concat(Extract(7, 7, v1), Extract(7, 0, v1))) == Extract(8, 8, Concat(Extract(7, 7, v0), Extract(7, 0, v0))*511 + Concat(Extract(7, 7, v1), Extract(7, 0, v1))), 1, 0), 1, 0)) */
#include <cstdint>

extern "C"
uint64_t
emu_setl_gpr_one_8__reg_rdi__cpp__native_first(uint8_t a, uint8_t b, uint64_t c)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = ((uint32_t)((uint32_t)a >> 7) & UINT32_C(0x1));
    uint32_t v2 = ((uint32_t)(((uint32_t)(v1) << 8) | (uint32_t)(v0)) & UINT32_C(0x1ff));
    uint32_t v3 = (uint32_t)b;
    uint32_t v4 = ((uint32_t)((uint32_t)b >> 7) & UINT32_C(0x1));
    uint32_t v5 = ((uint32_t)(((uint32_t)(v4) << 8) | (uint32_t)(v3)) & UINT32_C(0x1ff));
    uint32_t v6 = ((uint32_t)((uint32_t)(v5) * (uint32_t)(UINT32_C(0x1ff))) & UINT32_C(0x1ff));
    uint32_t v7 = ((uint32_t)((uint32_t)(v6) + (uint32_t)(v2)) & UINT32_C(0x1ff));
    uint32_t v8 = ((uint32_t)((uint32_t)(v7) >> 8) & UINT32_C(0x1));
    uint32_t v9 = ((uint32_t)((uint32_t)(v7) >> 7) & UINT32_C(0x1));
    int v10 = (((uint32_t)(v9) == (uint32_t)(v8))) ? 1 : 0;
    uint32_t v11 = ((v10) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0)));
    uint32_t v12 = ((uint32_t)((uint32_t)(v3) * (uint32_t)(UINT32_C(0xff))) & UINT32_C(0xff));
    uint32_t v13 = ((uint32_t)((uint32_t)(v12) + (uint32_t)(v0)) & UINT32_C(0xff));
    uint32_t v14 = ((uint32_t)((uint32_t)(v13) >> 7) & UINT32_C(0x1));
    int v15 = (((uint32_t)(v14) == (uint32_t)(v11))) ? 1 : 0;
    uint32_t v16 = ((v15) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0)));
    uint64_t v17 = ((uint64_t)((uint64_t)c >> 8) & UINT64_C(0xffffffffffffff));
    uint64_t v18 = (uint64_t)(((uint64_t)(v17) << 8) | (uint64_t)(v16));
    return (uint64_t)(v18);
}
