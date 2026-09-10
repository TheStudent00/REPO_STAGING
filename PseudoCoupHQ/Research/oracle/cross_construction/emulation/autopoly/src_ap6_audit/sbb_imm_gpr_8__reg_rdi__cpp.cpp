/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of sbb_imm_gpr_8__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(7, 0, v2)*255 + If(Extract(8, 8, Concat(0, Extract(7, 0, v0)) + Concat(0, Extract(7, 0, v1))) == 1, 1, 0)*255 + Extract(7, 0, v3)) */
#include <cstdint>

extern "C"
uint64_t
emu_sbb_imm_gpr_8__reg_rdi__cpp(uint8_t a, uint8_t b, uint8_t c, uint8_t d)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 8) | (uint64_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)((uint32_t)d) * (uint32_t)(UINT32_C(0xff))) & UINT32_C(0xff))) + (uint32_t)(((uint32_t)((uint32_t)(((((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)((uint32_t)b)) & UINT32_C(0x1ff))) + (uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)((uint32_t)a)) & UINT32_C(0x1ff)))) & UINT32_C(0x1ff))) >> 8) & UINT32_C(0x1))) == (uint32_t)(UINT32_C(0x1)))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0)))) * (uint32_t)(UINT32_C(0xff))) & UINT32_C(0xff))) + (uint32_t)((uint32_t)c)) & UINT32_C(0xff)))));
}
