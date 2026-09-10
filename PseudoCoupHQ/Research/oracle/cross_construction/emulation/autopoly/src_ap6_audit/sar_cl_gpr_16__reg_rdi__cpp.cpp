/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of sar_cl_gpr_16__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(15, 0, v0) >> Concat(0, Extract(4, 0, v1))) */
#include <cstdint>

extern "C"
uint64_t
emu_sar_cl_gpr_16__reg_rdi__cpp(uint16_t a, uint8_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 16) | (uint64_t)((((uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0xffff))) < (uint32_t)16) ? ((uint32_t)(((int32_t)((uint32_t)((uint32_t)a) << 16) >> 16) >> (unsigned)(uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0xffff)))) & UINT32_C(0xffff)) : ((((int32_t)((uint32_t)((uint32_t)a) << 16) >> 16) < 0) ? UINT32_C(0xffff) : (uint32_t)0)))));
}
