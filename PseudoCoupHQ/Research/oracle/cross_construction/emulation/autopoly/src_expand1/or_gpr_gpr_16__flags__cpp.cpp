/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of or_gpr_gpr_16__flags__cpp.  The term's layer-5 text, LITERAL:
   Concat(Extract(15, 0, v0) | Extract(15, 0, v1), 0) */
#include <cstdint>

extern "C"
uint32_t
emu_or_gpr_gpr_16__flags__cpp(uint16_t a, uint16_t b)
{
    return (uint32_t)((uint32_t)(((uint32_t)(((uint32_t)((uint32_t)((uint32_t)a) | (uint32_t)((uint32_t)b)) & UINT32_C(0xffff))) << 16) | (uint32_t)(UINT32_C(0x0))));
}
