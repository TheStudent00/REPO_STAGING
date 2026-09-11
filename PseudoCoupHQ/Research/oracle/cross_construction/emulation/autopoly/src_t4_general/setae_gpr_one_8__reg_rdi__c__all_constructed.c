/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of setae_gpr_one_8__reg_rdi__c__all_constructed.  The term's text, LITERAL:
   Concat(Extract(63, 8, v0), If(ULE(Extract(7, 0, v1), Extract(7, 0, v2)), 1, 0)) */
#include <stdint.h>

uint64_t
emu_setae_gpr_one_8__reg_rdi__c__all_constructed(uint8_t a, uint8_t b, uint64_t c)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = (uint32_t)b;
    uint32_t v2 = (uint32_t)(UINT32_C(0x1));
    uint32_t v3 = ((uint32_t)(~(uint32_t)(v1)) & UINT32_C(0xff));
    uint32_t v4 = ((uint32_t)((uint32_t)(v0) ^ (uint32_t)(v3)) & UINT32_C(0xff));
    uint32_t v5 = ((uint32_t)((uint32_t)(v4) & (uint32_t)(v2)) & UINT32_C(0xff));
    uint32_t v6 = ((uint32_t)((uint32_t)(v0) & (uint32_t)(v3)) & UINT32_C(0xff));
    uint32_t v7 = ((uint32_t)((uint32_t)(v6) | (uint32_t)(v5)) & UINT32_C(0xff));
    uint32_t v8 = ((uint32_t)((uint32_t)(v7) << (unsigned)(uint32_t)(UINT32_C(0x1))) & UINT32_C(0xff));
    uint32_t v9 = ((uint32_t)((uint32_t)(v4) & (uint32_t)(v8)) & UINT32_C(0xff));
    uint32_t v10 = ((uint32_t)((uint32_t)(v7) | (uint32_t)(v9)) & UINT32_C(0xff));
    uint32_t v11 = ((uint32_t)((uint32_t)(v10) << (unsigned)(uint32_t)(UINT32_C(0x2))) & UINT32_C(0xff));
    uint32_t v12 = ((uint32_t)((uint32_t)(v4) << (unsigned)(uint32_t)(UINT32_C(0x1))) & UINT32_C(0xff));
    uint32_t v13 = ((uint32_t)((uint32_t)(v4) & (uint32_t)(v12)) & UINT32_C(0xff));
    uint32_t v14 = ((uint32_t)((uint32_t)(v13) & (uint32_t)(v11)) & UINT32_C(0xff));
    uint32_t v15 = ((uint32_t)((uint32_t)(v10) | (uint32_t)(v14)) & UINT32_C(0xff));
    uint32_t v16 = ((uint32_t)((uint32_t)(v15) << (unsigned)(uint32_t)(UINT32_C(0x4))) & UINT32_C(0xff));
    uint32_t v17 = ((uint32_t)((uint32_t)(v13) << (unsigned)(uint32_t)(UINT32_C(0x2))) & UINT32_C(0xff));
    uint32_t v18 = ((uint32_t)((uint32_t)(v13) & (uint32_t)(v17)) & UINT32_C(0xff));
    uint32_t v19 = ((uint32_t)((uint32_t)(v18) & (uint32_t)(v16)) & UINT32_C(0xff));
    uint32_t v20 = ((uint32_t)((uint32_t)(v15) | (uint32_t)(v19)) & UINT32_C(0xff));
    uint32_t v21 = ((uint32_t)((uint32_t)(v20) >> 7) & UINT32_C(0x1));
    int v22 = (((uint32_t)(UINT32_C(0x0)) == (uint32_t)(v21))) ? 1 : 0;
    int v23 = ((!(v22))) ? 1 : 0;
    uint32_t v24 = ((v23) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0)));
    uint64_t v25 = ((uint64_t)((uint64_t)c >> 8) & UINT64_C(0xffffffffffffff));
    uint32_t v26 = v24;
    uint64_t v27 = v25;
    uint64_t v28 = (uint64_t)(((uint64_t)(v27) << 8) | (uint64_t)(v26));
    return (uint64_t)(v28);
}
