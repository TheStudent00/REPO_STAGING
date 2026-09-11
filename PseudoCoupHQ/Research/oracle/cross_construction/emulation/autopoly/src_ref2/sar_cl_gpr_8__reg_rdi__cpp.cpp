/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of sar_cl_gpr_8__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 8, v0), Extract(7, 0, v0) >> Concat(0, Extract(4, 0, v1))) */
#include <cstdint>

extern "C"
uint64_t
emu_sar_cl_gpr_8__reg_rdi__cpp(uint64_t a, uint8_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(((uint64_t)((uint64_t)a >> 8) & UINT64_C(0xffffffffffffff))) << 8) | (uint64_t)((((uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0xff))) < (uint32_t)8) ? ((uint32_t)(((int32_t)((uint32_t)(((uint32_t)((uint64_t)a >> 0) & UINT32_C(0xff))) << 24) >> 24) >> (unsigned)(uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0xff)))) & UINT32_C(0xff)) : ((((int32_t)((uint32_t)(((uint32_t)((uint64_t)a >> 0) & UINT32_C(0xff))) << 24) >> 24) < 0) ? UINT32_C(0xff) : (uint32_t)0)))));
}
