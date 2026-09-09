/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of cmp_imm_gpr_8__flags__cpp.  The term's layer-5 text, LITERAL:
   Concat(Extract(7, 0, v0), 3) */
#include <cstdint>

extern "C"
uint16_t
emu_cmp_imm_gpr_8__flags__cpp(uint8_t a)
{
    return (uint16_t)(((uint32_t)(((uint32_t)((uint32_t)a) << 8) | (uint32_t)(UINT32_C(0x3))) & UINT32_C(0xffff)));
}
