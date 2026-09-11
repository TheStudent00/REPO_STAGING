/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of shr_cl_gpr_32__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   Concat(0, LShR(Extract(31, 0, v0), Concat(0, Extract(4, 0, v1)))) */
#include <cstdint>

extern "C"
uint64_t
emu_shr_cl_gpr_32__reg_rdi__cpp(uint32_t a, uint8_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((uint32_t)((uint32_t)a) >> (unsigned)(uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))))))));
}
