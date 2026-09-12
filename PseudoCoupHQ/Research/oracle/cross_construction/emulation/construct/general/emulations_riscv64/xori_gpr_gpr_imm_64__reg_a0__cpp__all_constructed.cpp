/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of xori_gpr_gpr_imm_64__reg_a0__cpp__all_constructed.  The term's text, LITERAL:
   Concat(Extract(63, 2, v0), ~Extract(1, 0, v0)) */
#include <cstdint>

extern "C"
uint64_t
emu_xori_gpr_gpr_imm_64__reg_a0__cpp__all_constructed(uint64_t a)
{
    uint32_t v0 = ((uint32_t)((uint64_t)a >> 0) & UINT32_C(0x3));
    uint32_t v1 = ((uint32_t)(~(uint32_t)(v0)) & UINT32_C(0x3));
    uint64_t v2 = ((uint64_t)((uint64_t)a >> 2) & UINT64_C(0x3fffffffffffffff));
    uint32_t v3 = v1;
    uint64_t v4 = v2;
    uint64_t v5 = (uint64_t)(((uint64_t)(v4) << 2) | (uint64_t)(v3));
    return (uint64_t)(v5);
}
