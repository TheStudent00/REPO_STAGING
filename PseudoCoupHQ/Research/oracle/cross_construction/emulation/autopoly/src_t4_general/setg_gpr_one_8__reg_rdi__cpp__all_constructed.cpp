/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of setg_gpr_one_8__reg_rdi__cpp__all_constructed.  The term's text, LITERAL:
   Concat(Extract(63, 8, v2), If(And(Not(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) == 0), Or(Extract(7, 7, v0) == 0, Extract(7, 7, v1) == 0)), 1, 0)) */
#include <cstdint>

extern "C"
uint64_t
emu_setg_gpr_one_8__reg_rdi__cpp__all_constructed(uint8_t a, uint8_t b, uint64_t c)
{
    uint32_t v0 = ((uint32_t)((uint32_t)a >> 7) & UINT32_C(0x1));
    uint32_t v1 = ((uint32_t)((uint32_t)(v0) ^ (uint32_t)(UINT32_C(0x0))) & UINT32_C(0x1));
    uint32_t v2 = v1;
    int v3 = (((uint32_t)(UINT32_C(0x1)) == (uint32_t)(v2))) ? 1 : 0;
    int v4 = ((!(v3))) ? 1 : 0;
    uint32_t v5 = ((uint32_t)((uint32_t)b >> 7) & UINT32_C(0x1));
    uint32_t v6 = ((uint32_t)((uint32_t)(v5) ^ (uint32_t)(UINT32_C(0x0))) & UINT32_C(0x1));
    uint32_t v7 = v6;
    int v8 = (((uint32_t)(UINT32_C(0x1)) == (uint32_t)(v7))) ? 1 : 0;
    int v9 = ((!(v8))) ? 1 : 0;
    int v10 = (((v9) || (v4))) ? 1 : 0;
    uint32_t v11 = (uint32_t)a;
    uint32_t v12 = ((uint32_t)(~(uint32_t)(v11)) & UINT32_C(0xff));
    uint32_t v13 = (uint32_t)b;
    uint32_t v14 = ((uint32_t)(~(uint32_t)(v13)) & UINT32_C(0xff));
    uint32_t v15 = ((uint32_t)((uint32_t)(v14) | (uint32_t)(v12)) & UINT32_C(0xff));
    uint32_t v16 = ((uint32_t)(~(uint32_t)(v15)) & UINT32_C(0xff));
    uint32_t v17 = ((uint32_t)((uint32_t)(v16) ^ (uint32_t)(UINT32_C(0x0))) & UINT32_C(0xff));
    uint32_t v18 = ((uint32_t)((uint32_t)(v17) >> (unsigned)(uint32_t)(UINT32_C(0x1))) & UINT32_C(0xff));
    uint32_t v19 = ((uint32_t)((uint32_t)(v17) | (uint32_t)(v18)) & UINT32_C(0xff));
    uint32_t v20 = ((uint32_t)((uint32_t)(v19) >> (unsigned)(uint32_t)(UINT32_C(0x2))) & UINT32_C(0xff));
    uint32_t v21 = ((uint32_t)((uint32_t)(v19) | (uint32_t)(v20)) & UINT32_C(0xff));
    uint32_t v22 = ((uint32_t)((uint32_t)(v21) >> (unsigned)(uint32_t)(UINT32_C(0x4))) & UINT32_C(0xff));
    uint32_t v23 = ((uint32_t)((uint32_t)(v21) | (uint32_t)(v22)) & UINT32_C(0xff));
    uint32_t v24 = ((uint32_t)((uint32_t)(v23) >> 0) & UINT32_C(0x1));
    int v25 = (((uint32_t)(UINT32_C(0x1)) == (uint32_t)(v24))) ? 1 : 0;
    int v26 = ((!(v25))) ? 1 : 0;
    int v27 = ((!(v26))) ? 1 : 0;
    int v28 = (((v27) && (v10))) ? 1 : 0;
    uint32_t v29 = ((v28) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0)));
    uint64_t v30 = ((uint64_t)((uint64_t)c >> 8) & UINT64_C(0xffffffffffffff));
    uint32_t v31 = v29;
    uint64_t v32 = v30;
    uint64_t v33 = (uint64_t)(((uint64_t)(v32) << 8) | (uint64_t)(v31));
    return (uint64_t)(v33);
}
