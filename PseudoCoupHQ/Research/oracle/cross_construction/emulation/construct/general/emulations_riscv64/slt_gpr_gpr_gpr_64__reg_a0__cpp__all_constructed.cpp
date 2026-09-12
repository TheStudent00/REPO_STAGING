/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of slt_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed.  The term's text, LITERAL:
   If(v0 <= v1, 0, 1) */
#include <cstdint>

extern "C"
uint64_t
emu_slt_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed(uint64_t a, uint64_t b)
{
    uint64_t v0 = (uint64_t)(UINT32_C(0x1));
    uint64_t v1 = (uint64_t)((uint64_t)((uint64_t)b) ^ (uint64_t)(UINT64_C(0x8000000000000000)));
    uint64_t v2 = (uint64_t)(~(uint64_t)(v1));
    uint64_t v3 = (uint64_t)((uint64_t)((uint64_t)a) ^ (uint64_t)(UINT64_C(0x8000000000000000)));
    uint64_t v4 = (uint64_t)((uint64_t)(v3) ^ (uint64_t)(v2));
    uint64_t v5 = (uint64_t)((uint64_t)(v4) & (uint64_t)(v0));
    uint64_t v6 = (uint64_t)((uint64_t)(v3) & (uint64_t)(v2));
    uint64_t v7 = (uint64_t)((uint64_t)(v6) | (uint64_t)(v5));
    uint64_t v8 = (uint64_t)((uint64_t)(v7) << (unsigned)(uint64_t)(UINT64_C(0x1)));
    uint64_t v9 = (uint64_t)((uint64_t)(v4) & (uint64_t)(v8));
    uint64_t v10 = (uint64_t)((uint64_t)(v7) | (uint64_t)(v9));
    uint64_t v11 = (uint64_t)((uint64_t)(v10) << (unsigned)(uint64_t)(UINT64_C(0x2)));
    uint64_t v12 = (uint64_t)((uint64_t)(v4) << (unsigned)(uint64_t)(UINT64_C(0x1)));
    uint64_t v13 = (uint64_t)((uint64_t)(v4) & (uint64_t)(v12));
    uint64_t v14 = (uint64_t)((uint64_t)(v13) & (uint64_t)(v11));
    uint64_t v15 = (uint64_t)((uint64_t)(v10) | (uint64_t)(v14));
    uint64_t v16 = (uint64_t)((uint64_t)(v15) << (unsigned)(uint64_t)(UINT64_C(0x4)));
    uint64_t v17 = (uint64_t)((uint64_t)(v13) << (unsigned)(uint64_t)(UINT64_C(0x2)));
    uint64_t v18 = (uint64_t)((uint64_t)(v13) & (uint64_t)(v17));
    uint64_t v19 = (uint64_t)((uint64_t)(v18) & (uint64_t)(v16));
    uint64_t v20 = (uint64_t)((uint64_t)(v15) | (uint64_t)(v19));
    uint64_t v21 = (uint64_t)((uint64_t)(v20) << (unsigned)(uint64_t)(UINT64_C(0x8)));
    uint64_t v22 = (uint64_t)((uint64_t)(v18) << (unsigned)(uint64_t)(UINT64_C(0x4)));
    uint64_t v23 = (uint64_t)((uint64_t)(v18) & (uint64_t)(v22));
    uint64_t v24 = (uint64_t)((uint64_t)(v23) & (uint64_t)(v21));
    uint64_t v25 = (uint64_t)((uint64_t)(v20) | (uint64_t)(v24));
    uint64_t v26 = (uint64_t)((uint64_t)(v25) << (unsigned)(uint64_t)(UINT64_C(0x10)));
    uint64_t v27 = (uint64_t)((uint64_t)(v23) << (unsigned)(uint64_t)(UINT64_C(0x8)));
    uint64_t v28 = (uint64_t)((uint64_t)(v23) & (uint64_t)(v27));
    uint64_t v29 = (uint64_t)((uint64_t)(v28) & (uint64_t)(v26));
    uint64_t v30 = (uint64_t)((uint64_t)(v25) | (uint64_t)(v29));
    uint64_t v31 = (uint64_t)((uint64_t)(v30) << (unsigned)(uint64_t)(UINT64_C(0x20)));
    uint64_t v32 = (uint64_t)((uint64_t)(v28) << (unsigned)(uint64_t)(UINT64_C(0x10)));
    uint64_t v33 = (uint64_t)((uint64_t)(v28) & (uint64_t)(v32));
    uint64_t v34 = (uint64_t)((uint64_t)(v33) & (uint64_t)(v31));
    uint64_t v35 = (uint64_t)((uint64_t)(v30) | (uint64_t)(v34));
    uint32_t v36 = ((uint32_t)((uint64_t)(v35) >> 63) & UINT32_C(0x1));
    int v37 = (((uint32_t)(UINT32_C(0x0)) == (uint32_t)(v36))) ? 1 : 0;
    int v38 = ((!(v37))) ? 1 : 0;
    uint64_t v39 = ((v38) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)(UINT64_C(0x1)));
    return (uint64_t)(v39);
}
