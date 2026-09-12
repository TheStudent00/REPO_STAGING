/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of sw_gpr_mem_32__mem_MEM_0x0_a1___c__all_constructed.  The term's text, LITERAL:
   Concat(Extract(63, 32, v0), Extract(31, 0, v1)) */
#include <stdint.h>

uint64_t
emu_sw_gpr_mem_32__mem_MEM_0x0_a1___c__all_constructed(uint64_t a, uint32_t b)
{
    uint32_t v0 = (uint32_t)b;
    uint32_t v1 = (uint32_t)((uint64_t)a >> 32);
    uint32_t v2 = v0;
    uint32_t v3 = v1;
    uint64_t v4 = (uint64_t)(((uint64_t)(v3) << 32) | (uint64_t)(v2));
    return (uint64_t)(v4);
}
