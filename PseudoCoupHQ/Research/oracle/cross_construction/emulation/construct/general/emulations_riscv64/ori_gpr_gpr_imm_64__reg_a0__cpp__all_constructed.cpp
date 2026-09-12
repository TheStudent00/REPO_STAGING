/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of ori_gpr_gpr_imm_64__reg_a0__cpp__all_constructed.  The term's text, LITERAL:
   Concat(Extract(63, 2, v0), 3) */
#include <cstdint>

extern "C"
uint64_t
emu_ori_gpr_gpr_imm_64__reg_a0__cpp__all_constructed(uint64_t a)
{
    uint64_t v0 = ((uint64_t)((uint64_t)a >> 2) & UINT64_C(0x3fffffffffffffff));
    uint32_t v1 = UINT32_C(0x3);
    uint64_t v2 = v0;
    uint64_t v3 = (uint64_t)(((uint64_t)(v2) << 2) | (uint64_t)(v1));
    return (uint64_t)(v3);
}
