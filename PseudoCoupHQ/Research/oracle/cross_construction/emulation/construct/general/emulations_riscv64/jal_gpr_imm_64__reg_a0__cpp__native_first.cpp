/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of jal_gpr_imm_64__reg_a0__cpp__native_first.  The term's text, LITERAL:
   v0 + 4 */
#include <cstdint>

extern "C"
uint64_t
emu_jal_gpr_imm_64__reg_a0__cpp__native_first(uint64_t a)
{
    uint64_t v0 = (uint64_t)((uint64_t)((uint64_t)a) + (uint64_t)(UINT64_C(0x4)));
    return (uint64_t)(v0);
}
