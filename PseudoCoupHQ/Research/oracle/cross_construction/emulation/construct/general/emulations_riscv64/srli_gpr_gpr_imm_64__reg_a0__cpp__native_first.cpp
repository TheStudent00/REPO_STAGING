/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of srli_gpr_gpr_imm_64__reg_a0__cpp__native_first.  The term's text, LITERAL:
   Concat(0, Extract(63, 3, v0)) */
#include <cstdint>

extern "C"
uint64_t
emu_srli_gpr_gpr_imm_64__reg_a0__cpp__native_first(uint64_t a)
{
    uint64_t v0 = ((uint64_t)((uint64_t)a >> 3) & UINT64_C(0x1fffffffffffffff));
    uint64_t v1 = (uint64_t)(((uint64_t)(UINT32_C(0x0)) << 61) | (uint64_t)(v0));
    return (uint64_t)(v1);
}
