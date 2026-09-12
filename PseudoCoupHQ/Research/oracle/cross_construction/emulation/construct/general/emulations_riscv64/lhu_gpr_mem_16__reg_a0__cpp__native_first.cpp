/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of lhu_gpr_mem_16__reg_a0__cpp__native_first.  The term's text, LITERAL:
   Concat(0, Extract(15, 0, v0)) */
#include <cstdint>

extern "C"
uint64_t
emu_lhu_gpr_mem_16__reg_a0__cpp__native_first(uint16_t a)
{
    uint32_t v0 = (uint32_t)a;
    uint64_t v1 = (uint64_t)(((uint64_t)(UINT64_C(0x0)) << 16) | (uint64_t)(v0));
    return (uint64_t)(v1);
}
