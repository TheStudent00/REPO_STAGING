/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of seta_gpr_one_8__reg_rdi__cpp__all_constructed.  The term's text, LITERAL:
   Concat(Extract(63, 8, v2), If(And(ULE(Extract(7, 0, v0), Extract(7, 0, v1)), Not(Extract(7, 0, v0) == Extract(7, 0, v1))), 1, 0)) */
#include <cstdint>

extern "C"
uint64_t
emu_seta_gpr_one_8__reg_rdi__cpp__all_constructed(uint8_t a, uint8_t b, uint64_t c)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = (uint32_t)b;
    uint32_t v2 = ((uint32_t)((uint32_t)(v1) ^ (uint32_t)(v0)) & UINT32_C(0xff));
    uint32_t v3 = ((uint32_t)((uint32_t)(v2) >> (unsigned)(uint32_t)(UINT32_C(0x1))) & UINT32_C(0xff));
    uint32_t v4 = ((uint32_t)((uint32_t)(v2) | (uint32_t)(v3)) & UINT32_C(0xff));
    uint32_t v5 = ((uint32_t)((uint32_t)(v4) >> (unsigned)(uint32_t)(UINT32_C(0x2))) & UINT32_C(0xff));
    uint32_t v6 = ((uint32_t)((uint32_t)(v4) | (uint32_t)(v5)) & UINT32_C(0xff));
    uint32_t v7 = ((uint32_t)((uint32_t)(v6) >> (unsigned)(uint32_t)(UINT32_C(0x4))) & UINT32_C(0xff));
    uint32_t v8 = ((uint32_t)((uint32_t)(v6) | (uint32_t)(v7)) & UINT32_C(0xff));
    uint32_t v9 = ((uint32_t)((uint32_t)(v8) >> 0) & UINT32_C(0x1));
    int v10 = (((uint32_t)(UINT32_C(0x1)) == (uint32_t)(v9))) ? 1 : 0;
    int v11 = ((!(v10))) ? 1 : 0;
    int v12 = ((!(v11))) ? 1 : 0;
    uint32_t v13 = (uint32_t)(UINT32_C(0x1));
    uint32_t v14 = ((uint32_t)(~(uint32_t)(v1)) & UINT32_C(0xff));
    uint32_t v15 = ((uint32_t)((uint32_t)(v0) ^ (uint32_t)(v14)) & UINT32_C(0xff));
    uint32_t v16 = ((uint32_t)((uint32_t)(v15) & (uint32_t)(v13)) & UINT32_C(0xff));
    uint32_t v17 = ((uint32_t)((uint32_t)(v0) & (uint32_t)(v14)) & UINT32_C(0xff));
    uint32_t v18 = ((uint32_t)((uint32_t)(v17) | (uint32_t)(v16)) & UINT32_C(0xff));
    uint32_t v19 = ((uint32_t)((uint32_t)(v18) << (unsigned)(uint32_t)(UINT32_C(0x1))) & UINT32_C(0xff));
    uint32_t v20 = ((uint32_t)((uint32_t)(v15) & (uint32_t)(v19)) & UINT32_C(0xff));
    uint32_t v21 = ((uint32_t)((uint32_t)(v18) | (uint32_t)(v20)) & UINT32_C(0xff));
    uint32_t v22 = ((uint32_t)((uint32_t)(v21) << (unsigned)(uint32_t)(UINT32_C(0x2))) & UINT32_C(0xff));
    uint32_t v23 = ((uint32_t)((uint32_t)(v15) << (unsigned)(uint32_t)(UINT32_C(0x1))) & UINT32_C(0xff));
    uint32_t v24 = ((uint32_t)((uint32_t)(v15) & (uint32_t)(v23)) & UINT32_C(0xff));
    uint32_t v25 = ((uint32_t)((uint32_t)(v24) & (uint32_t)(v22)) & UINT32_C(0xff));
    uint32_t v26 = ((uint32_t)((uint32_t)(v21) | (uint32_t)(v25)) & UINT32_C(0xff));
    uint32_t v27 = ((uint32_t)((uint32_t)(v26) << (unsigned)(uint32_t)(UINT32_C(0x4))) & UINT32_C(0xff));
    uint32_t v28 = ((uint32_t)((uint32_t)(v24) << (unsigned)(uint32_t)(UINT32_C(0x2))) & UINT32_C(0xff));
    uint32_t v29 = ((uint32_t)((uint32_t)(v24) & (uint32_t)(v28)) & UINT32_C(0xff));
    uint32_t v30 = ((uint32_t)((uint32_t)(v29) & (uint32_t)(v27)) & UINT32_C(0xff));
    uint32_t v31 = ((uint32_t)((uint32_t)(v26) | (uint32_t)(v30)) & UINT32_C(0xff));
    uint32_t v32 = ((uint32_t)((uint32_t)(v31) >> 7) & UINT32_C(0x1));
    int v33 = (((uint32_t)(UINT32_C(0x0)) == (uint32_t)(v32))) ? 1 : 0;
    int v34 = ((!(v33))) ? 1 : 0;
    int v35 = (((v34) && (v12))) ? 1 : 0;
    uint32_t v36 = ((v35) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0)));
    uint64_t v37 = ((uint64_t)((uint64_t)c >> 8) & UINT64_C(0xffffffffffffff));
    uint32_t v38 = v36;
    uint64_t v39 = v37;
    uint64_t v40 = (uint64_t)(((uint64_t)(v39) << 8) | (uint64_t)(v38));
    return (uint64_t)(v40);
}
