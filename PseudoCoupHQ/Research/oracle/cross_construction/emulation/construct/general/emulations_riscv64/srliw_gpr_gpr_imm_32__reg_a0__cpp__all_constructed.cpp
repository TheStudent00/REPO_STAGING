/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of srliw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed.  The term's text, LITERAL:
   Concat(0, Extract(31, 3, v0)) */
#include <cstdint>

extern "C"
uint64_t
emu_srliw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed(uint32_t a)
{
    uint32_t v0 = ((uint32_t)((uint32_t)a >> 3) & UINT32_C(0x1fffffff));
    uint32_t v1 = v0;
    uint64_t v2 = UINT64_C(0x0);
    uint64_t v3 = (uint64_t)(((uint64_t)(v2) << 29) | (uint64_t)(v1));
    return (uint64_t)(v3);
}
