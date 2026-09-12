/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of lbu_gpr_fpr_fpr_8__reg_a0__cpp__all_constructed.  The term's text, LITERAL:
   Concat(0, Extract(7, 0, v0)) */
#include <cstdint>

extern "C"
uint64_t
emu_lbu_gpr_fpr_fpr_8__reg_a0__cpp__all_constructed(uint8_t a)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = v0;
    uint64_t v2 = UINT64_C(0x0);
    uint64_t v3 = (uint64_t)(((uint64_t)(v2) << 8) | (uint64_t)(v1));
    return (uint64_t)(v3);
}
