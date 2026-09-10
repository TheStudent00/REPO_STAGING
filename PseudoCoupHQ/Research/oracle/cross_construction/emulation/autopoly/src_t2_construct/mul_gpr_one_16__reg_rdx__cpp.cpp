/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of mul_gpr_one_16__reg_rdx__cpp.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 16, v2), Extract(31, 16, Concat(0, Extract(15, 0, v0))*Concat(0, Extract(15, 0, v1)))) */
#include <cstdint>

extern "C"
uint64_t
emu_mul_gpr_one_16__reg_rdx__cpp(uint16_t a, uint16_t b, uint64_t c)
{
    return (uint64_t)((uint64_t)(((uint64_t)(((uint64_t)((uint64_t)c >> 16) & UINT64_C(0xffffffffffff))) << 16) | (uint64_t)(((uint32_t)((uint32_t)((uint32_t)((uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)((uint32_t)a))) * (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)((uint32_t)b))))) >> 16) & UINT32_C(0xffff)))));
}
