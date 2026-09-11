/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of or_gpr_gpr_8__flags__cpp.  The term's layer-5 text, LITERAL:
   Concat(Extract(7, 0, v0) | Extract(7, 0, v1), 0) */
#include <cstdint>

extern "C"
uint16_t
emu_or_gpr_gpr_8__flags__cpp(uint8_t a, uint8_t b)
{
    return (uint16_t)(((uint32_t)(((uint32_t)(((uint32_t)((uint32_t)((uint32_t)a) | (uint32_t)((uint32_t)b)) & UINT32_C(0xff))) << 8) | (uint32_t)(UINT32_C(0x0))) & UINT32_C(0xffff)));
}
