/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of jalr_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed.  The term's text, LITERAL:
   v0 + 4 */
#include <cstdint>

extern "C"
uint64_t
emu_jalr_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed(uint64_t a)
{
    uint64_t v0 = (uint64_t)((uint64_t)((uint64_t)a) & (uint64_t)(UINT64_C(0x4)));
    uint64_t v1 = (uint64_t)((uint64_t)(v0) << (unsigned)(uint64_t)(UINT64_C(0x1)));
    uint64_t v2 = (uint64_t)((uint64_t)((uint64_t)a) ^ (uint64_t)(UINT64_C(0x4)));
    uint64_t v3 = (uint64_t)((uint64_t)(v2) & (uint64_t)(v1));
    uint64_t v4 = (uint64_t)((uint64_t)(v0) | (uint64_t)(v3));
    uint64_t v5 = (uint64_t)((uint64_t)(v4) << (unsigned)(uint64_t)(UINT64_C(0x2)));
    uint64_t v6 = (uint64_t)((uint64_t)(v2) << (unsigned)(uint64_t)(UINT64_C(0x1)));
    uint64_t v7 = (uint64_t)((uint64_t)(v2) & (uint64_t)(v6));
    uint64_t v8 = (uint64_t)((uint64_t)(v7) & (uint64_t)(v5));
    uint64_t v9 = (uint64_t)((uint64_t)(v4) | (uint64_t)(v8));
    uint64_t v10 = (uint64_t)((uint64_t)(v9) << (unsigned)(uint64_t)(UINT64_C(0x4)));
    uint64_t v11 = (uint64_t)((uint64_t)(v7) << (unsigned)(uint64_t)(UINT64_C(0x2)));
    uint64_t v12 = (uint64_t)((uint64_t)(v7) & (uint64_t)(v11));
    uint64_t v13 = (uint64_t)((uint64_t)(v12) & (uint64_t)(v10));
    uint64_t v14 = (uint64_t)((uint64_t)(v9) | (uint64_t)(v13));
    uint64_t v15 = (uint64_t)((uint64_t)(v14) << (unsigned)(uint64_t)(UINT64_C(0x8)));
    uint64_t v16 = (uint64_t)((uint64_t)(v12) << (unsigned)(uint64_t)(UINT64_C(0x4)));
    uint64_t v17 = (uint64_t)((uint64_t)(v12) & (uint64_t)(v16));
    uint64_t v18 = (uint64_t)((uint64_t)(v17) & (uint64_t)(v15));
    uint64_t v19 = (uint64_t)((uint64_t)(v14) | (uint64_t)(v18));
    uint64_t v20 = (uint64_t)((uint64_t)(v19) << (unsigned)(uint64_t)(UINT64_C(0x10)));
    uint64_t v21 = (uint64_t)((uint64_t)(v17) << (unsigned)(uint64_t)(UINT64_C(0x8)));
    uint64_t v22 = (uint64_t)((uint64_t)(v17) & (uint64_t)(v21));
    uint64_t v23 = (uint64_t)((uint64_t)(v22) & (uint64_t)(v20));
    uint64_t v24 = (uint64_t)((uint64_t)(v19) | (uint64_t)(v23));
    uint64_t v25 = (uint64_t)((uint64_t)(v24) << (unsigned)(uint64_t)(UINT64_C(0x20)));
    uint64_t v26 = (uint64_t)((uint64_t)(v22) << (unsigned)(uint64_t)(UINT64_C(0x10)));
    uint64_t v27 = (uint64_t)((uint64_t)(v22) & (uint64_t)(v26));
    uint64_t v28 = (uint64_t)((uint64_t)(v27) & (uint64_t)(v25));
    uint64_t v29 = (uint64_t)((uint64_t)(v24) | (uint64_t)(v28));
    uint64_t v30 = (uint64_t)((uint64_t)(v29) << (unsigned)(uint64_t)(UINT64_C(0x1)));
    uint64_t v31 = (uint64_t)((uint64_t)(v2) ^ (uint64_t)(v30));
    return (uint64_t)(v31);
}
