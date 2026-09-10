/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of mul_gpr_one_16__reg_rax__cpp.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 16, v0), Extract(15, 0, v0)*Extract(15, 0, v1)) */
#include <cstdint>

extern "C"
uint64_t
emu_mul_gpr_one_16__reg_rax__cpp(uint64_t a, uint16_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(((uint64_t)((uint64_t)a >> 16) & UINT64_C(0xffffffffffff))) << 16) | (uint64_t)(((uint32_t)((uint32_t)(((uint32_t)((uint64_t)a >> 0) & UINT32_C(0xffff))) * (uint32_t)((uint32_t)b)) & UINT32_C(0xffff)))));
}
