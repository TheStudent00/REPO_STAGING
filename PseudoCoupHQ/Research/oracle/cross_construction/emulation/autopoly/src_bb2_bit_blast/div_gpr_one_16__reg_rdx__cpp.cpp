/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of div_gpr_one_16__reg_rdx__cpp.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 16, v0), Extract(15, 0, bvurem_i(Concat(Extract(15, 0, v0), Extract(15, 0, v1)), Concat(0, Extract(15, 0, v2))))) */
#include <cstdint>

extern "C"
uint64_t
emu_div_gpr_one_16__reg_rdx__cpp(uint64_t a, uint16_t b, uint16_t c)
{
    return (uint64_t)((uint64_t)(((uint64_t)(((uint64_t)((uint64_t)a >> 16) & UINT64_C(0xffffffffffff))) << 16) | (uint64_t)(((uint32_t)((uint32_t)((uint32_t)((uint32_t)((uint32_t)(((uint32_t)(((uint32_t)((uint64_t)a >> 0) & UINT32_C(0xffff))) << 16) | (uint32_t)((uint32_t)b))) % (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)((uint32_t)c))))) >> 0) & UINT32_C(0xffff)))));
}
