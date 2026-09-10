/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of cmp_gpr_gpr_16__flags__cpp.  The term's layer-5 text, LITERAL:
   Concat(Extract(15, 0, v0), Extract(15, 0, v1)) */
#include <cstdint>

extern "C"
uint32_t
emu_cmp_gpr_gpr_16__flags__cpp(uint16_t a, uint16_t b)
{
    return (uint32_t)((uint32_t)(((uint32_t)((uint32_t)a) << 16) | (uint32_t)((uint32_t)b)));
}
