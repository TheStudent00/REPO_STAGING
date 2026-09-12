/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of beq_gpr_gpr_64__branch_condition__cpp__all_constructed.  The term's text, LITERAL:
   If(v0 == v1, 1, 0) */
#include <cstdint>

extern "C"
uint64_t
emu_beq_gpr_gpr_64__branch_condition__cpp__all_constructed(uint64_t a, uint64_t b)
{
    uint64_t v0 = (uint64_t)((uint64_t)((uint64_t)a) ^ (uint64_t)((uint64_t)b));
    uint64_t v1 = (uint64_t)((uint64_t)(v0) >> (unsigned)(uint64_t)(UINT64_C(0x1)));
    uint64_t v2 = (uint64_t)((uint64_t)(v0) | (uint64_t)(v1));
    uint64_t v3 = (uint64_t)((uint64_t)(v2) >> (unsigned)(uint64_t)(UINT64_C(0x2)));
    uint64_t v4 = (uint64_t)((uint64_t)(v2) | (uint64_t)(v3));
    uint64_t v5 = (uint64_t)((uint64_t)(v4) >> (unsigned)(uint64_t)(UINT64_C(0x4)));
    uint64_t v6 = (uint64_t)((uint64_t)(v4) | (uint64_t)(v5));
    uint64_t v7 = (uint64_t)((uint64_t)(v6) >> (unsigned)(uint64_t)(UINT64_C(0x8)));
    uint64_t v8 = (uint64_t)((uint64_t)(v6) | (uint64_t)(v7));
    uint64_t v9 = (uint64_t)((uint64_t)(v8) >> (unsigned)(uint64_t)(UINT64_C(0x10)));
    uint64_t v10 = (uint64_t)((uint64_t)(v8) | (uint64_t)(v9));
    uint64_t v11 = (uint64_t)((uint64_t)(v10) >> (unsigned)(uint64_t)(UINT64_C(0x20)));
    uint64_t v12 = (uint64_t)((uint64_t)(v10) | (uint64_t)(v11));
    uint32_t v13 = ((uint32_t)((uint64_t)(v12) >> 0) & UINT32_C(0x1));
    int v14 = (((uint32_t)(UINT32_C(0x1)) == (uint32_t)(v13))) ? 1 : 0;
    int v15 = ((!(v14))) ? 1 : 0;
    uint64_t v16 = ((v15) ? (uint64_t)(UINT64_C(0x1)) : (uint64_t)(UINT64_C(0x0)));
    return (uint64_t)(v16);
}
