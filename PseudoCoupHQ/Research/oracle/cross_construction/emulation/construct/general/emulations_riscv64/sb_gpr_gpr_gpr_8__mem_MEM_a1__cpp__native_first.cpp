/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of sb_gpr_gpr_gpr_8__mem_MEM_a1__cpp__native_first.  The term's text, LITERAL:
   Concat(Extract(63, 8, v0), Extract(7, 0, v1)) */
#include <cstdint>

extern "C"
uint64_t
emu_sb_gpr_gpr_gpr_8__mem_MEM_a1__cpp__native_first(uint64_t a, uint8_t b)
{
    uint32_t v0 = (uint32_t)b;
    uint64_t v1 = ((uint64_t)((uint64_t)a >> 8) & UINT64_C(0xffffffffffffff));
    uint64_t v2 = (uint64_t)(((uint64_t)(v1) << 8) | (uint64_t)(v0));
    return (uint64_t)(v2);
}
