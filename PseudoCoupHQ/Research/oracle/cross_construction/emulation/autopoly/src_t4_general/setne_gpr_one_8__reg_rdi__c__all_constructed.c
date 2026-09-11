/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of setne_gpr_one_8__reg_rdi__c__all_constructed.  The term's text, LITERAL:
   Concat(Extract(63, 8, v2), If(Extract(7, 0, v0) | Extract(7, 0, v1) == 0, 0, 1)) */
#include <stdint.h>

uint64_t
emu_setne_gpr_one_8__reg_rdi__c__all_constructed(uint8_t a, uint8_t b, uint64_t c)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = (uint32_t)b;
    uint32_t v2 = ((uint32_t)((uint32_t)(v1) | (uint32_t)(v0)) & UINT32_C(0xff));
    uint32_t v3 = ((uint32_t)((uint32_t)(v2) ^ (uint32_t)(UINT32_C(0x0))) & UINT32_C(0xff));
    uint32_t v4 = ((uint32_t)((uint32_t)(v3) >> (unsigned)(uint32_t)(UINT32_C(0x1))) & UINT32_C(0xff));
    uint32_t v5 = ((uint32_t)((uint32_t)(v3) | (uint32_t)(v4)) & UINT32_C(0xff));
    uint32_t v6 = ((uint32_t)((uint32_t)(v5) >> (unsigned)(uint32_t)(UINT32_C(0x2))) & UINT32_C(0xff));
    uint32_t v7 = ((uint32_t)((uint32_t)(v5) | (uint32_t)(v6)) & UINT32_C(0xff));
    uint32_t v8 = ((uint32_t)((uint32_t)(v7) >> (unsigned)(uint32_t)(UINT32_C(0x4))) & UINT32_C(0xff));
    uint32_t v9 = ((uint32_t)((uint32_t)(v7) | (uint32_t)(v8)) & UINT32_C(0xff));
    uint32_t v10 = ((uint32_t)((uint32_t)(v9) >> 0) & UINT32_C(0x1));
    int v11 = (((uint32_t)(UINT32_C(0x1)) == (uint32_t)(v10))) ? 1 : 0;
    int v12 = ((!(v11))) ? 1 : 0;
    uint32_t v13 = ((v12) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1)));
    uint64_t v14 = ((uint64_t)((uint64_t)c >> 8) & UINT64_C(0xffffffffffffff));
    uint32_t v15 = v13;
    uint64_t v16 = v14;
    uint64_t v17 = (uint64_t)(((uint64_t)(v16) << 8) | (uint64_t)(v15));
    return (uint64_t)(v17);
}
