/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01598__rust_regen_1089.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 0, bvurem_i(Concat(0, Extract(31, 0, v0)), Concat(0, Extract(31, 0, v1))))) */
#include <stdint.h>

uint64_t
emu_E01598__rust_regen_1089(uint32_t a, uint32_t b, uint64_t c)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((uint64_t)((uint64_t)((uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)a))) % (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)b))))) >> 0))));
}
