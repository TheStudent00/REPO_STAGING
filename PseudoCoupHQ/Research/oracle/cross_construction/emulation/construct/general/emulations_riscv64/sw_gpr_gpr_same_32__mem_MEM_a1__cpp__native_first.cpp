/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of sw_gpr_gpr_same_32__mem_MEM_a1__cpp__native_first.  The term's text, LITERAL:
   Concat(Extract(63, 32, v0), Extract(31, 0, v1)) */
#include <cstdint>

extern "C"
uint64_t
emu_sw_gpr_gpr_same_32__mem_MEM_a1__cpp__native_first(uint64_t a, uint32_t b)
{
    uint32_t v0 = (uint32_t)b;
    uint32_t v1 = (uint32_t)((uint64_t)a >> 32);
    uint64_t v2 = (uint64_t)(((uint64_t)(v1) << 32) | (uint64_t)(v0));
    return (uint64_t)(v2);
}
