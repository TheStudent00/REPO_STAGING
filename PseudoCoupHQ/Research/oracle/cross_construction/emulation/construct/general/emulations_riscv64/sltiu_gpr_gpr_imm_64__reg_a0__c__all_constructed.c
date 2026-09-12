/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of sltiu_gpr_gpr_imm_64__reg_a0__c__all_constructed.  The term's text, LITERAL:
   If(Or(Extract(1, 0, v0) == 3, Not(Extract(63, 2, v0) == 0)), 0, 1) */
#include <stdint.h>

uint64_t
emu_sltiu_gpr_gpr_imm_64__reg_a0__c__all_constructed(uint64_t a)
{
    uint64_t v0 = ((uint64_t)((uint64_t)a >> 2) & UINT64_C(0x3fffffffffffffff));
    uint64_t v1 = ((uint64_t)((uint64_t)(v0) ^ (uint64_t)(UINT64_C(0x0))) & UINT64_C(0x3fffffffffffffff));
    uint64_t v2 = ((uint64_t)((uint64_t)(v1) >> (unsigned)(uint64_t)(UINT64_C(0x1))) & UINT64_C(0x3fffffffffffffff));
    uint64_t v3 = ((uint64_t)((uint64_t)(v1) | (uint64_t)(v2)) & UINT64_C(0x3fffffffffffffff));
    uint64_t v4 = ((uint64_t)((uint64_t)(v3) >> (unsigned)(uint64_t)(UINT64_C(0x2))) & UINT64_C(0x3fffffffffffffff));
    uint64_t v5 = ((uint64_t)((uint64_t)(v3) | (uint64_t)(v4)) & UINT64_C(0x3fffffffffffffff));
    uint64_t v6 = ((uint64_t)((uint64_t)(v5) >> (unsigned)(uint64_t)(UINT64_C(0x4))) & UINT64_C(0x3fffffffffffffff));
    uint64_t v7 = ((uint64_t)((uint64_t)(v5) | (uint64_t)(v6)) & UINT64_C(0x3fffffffffffffff));
    uint64_t v8 = ((uint64_t)((uint64_t)(v7) >> (unsigned)(uint64_t)(UINT64_C(0x8))) & UINT64_C(0x3fffffffffffffff));
    uint64_t v9 = ((uint64_t)((uint64_t)(v7) | (uint64_t)(v8)) & UINT64_C(0x3fffffffffffffff));
    uint64_t v10 = ((uint64_t)((uint64_t)(v9) >> (unsigned)(uint64_t)(UINT64_C(0x10))) & UINT64_C(0x3fffffffffffffff));
    uint64_t v11 = ((uint64_t)((uint64_t)(v9) | (uint64_t)(v10)) & UINT64_C(0x3fffffffffffffff));
    uint64_t v12 = ((uint64_t)((uint64_t)(v11) >> (unsigned)(uint64_t)(UINT64_C(0x20))) & UINT64_C(0x3fffffffffffffff));
    uint64_t v13 = ((uint64_t)((uint64_t)(v11) | (uint64_t)(v12)) & UINT64_C(0x3fffffffffffffff));
    uint32_t v14 = ((uint32_t)((uint64_t)(v13) >> 0) & UINT32_C(0x1));
    int v15 = (((uint32_t)(UINT32_C(0x1)) == (uint32_t)(v14))) ? 1 : 0;
    int v16 = ((!(v15))) ? 1 : 0;
    int v17 = ((!(v16))) ? 1 : 0;
    uint32_t v18 = ((uint32_t)((uint64_t)a >> 0) & UINT32_C(0x3));
    uint32_t v19 = ((uint32_t)((uint32_t)(v18) ^ (uint32_t)(UINT32_C(0x3))) & UINT32_C(0x3));
    uint32_t v20 = ((uint32_t)((uint32_t)(v19) >> (unsigned)(uint32_t)(UINT32_C(0x1))) & UINT32_C(0x3));
    uint32_t v21 = ((uint32_t)((uint32_t)(v19) | (uint32_t)(v20)) & UINT32_C(0x3));
    uint32_t v22 = ((uint32_t)((uint32_t)(v21) >> 0) & UINT32_C(0x1));
    int v23 = (((uint32_t)(UINT32_C(0x1)) == (uint32_t)(v22))) ? 1 : 0;
    int v24 = ((!(v23))) ? 1 : 0;
    int v25 = (((v24) || (v17))) ? 1 : 0;
    uint64_t v26 = ((v25) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)(UINT64_C(0x1)));
    return (uint64_t)(v26);
}
