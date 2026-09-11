/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of div_gpr_one_8__reg_rax__cpp.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 16, v0), Extract(7, 0, bvurem_i(Extract(15, 0, v0), Concat(0, Extract(7, 0, v1)))), Extract(7, 0, bvudiv_i(Extract(15, 0, v0), Concat(0, Extract(7, 0, v1))))) */
#include <cstdint>

extern "C"
uint64_t
emu_div_gpr_one_8__reg_rax__cpp(uint64_t a, uint8_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(((uint64_t)((uint64_t)a >> 16) & UINT64_C(0xffffffffffff))) << 16) | ((uint64_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint64_t)a >> 0) & UINT32_C(0xffff))) % (uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)((uint32_t)b)) & UINT32_C(0xffff)))) & UINT32_C(0xffff))) >> 0) & UINT32_C(0xff))) << 8) | (uint64_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint64_t)a >> 0) & UINT32_C(0xffff))) / (uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)((uint32_t)b)) & UINT32_C(0xffff)))) & UINT32_C(0xffff))) >> 0) & UINT32_C(0xff)))));
}
