/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of and_gpr_gpr_32__flags__cpp__all_constructed.  The term's text, LITERAL:
   Concat(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)), 0) */
#include <cstdint>

extern "C"
uint64_t
emu_and_gpr_gpr_32__flags__cpp__all_constructed(uint32_t a, uint32_t b)
{
    uint32_t v0 = (uint32_t)b;
    uint32_t v1 = (uint32_t)(~(uint32_t)(v0));
    uint32_t v2 = (uint32_t)a;
    uint32_t v3 = (uint32_t)(~(uint32_t)(v2));
    uint32_t v4 = (uint32_t)((uint32_t)(v3) | (uint32_t)(v1));
    uint32_t v5 = (uint32_t)(~(uint32_t)(v4));
    uint32_t v6 = UINT32_C(0x0);
    uint32_t v7 = v5;
    uint64_t v8 = (uint64_t)(((uint64_t)(v7) << 32) | (uint64_t)(v6));
    return (uint64_t)(v8);
}
