/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of movd_xmm_gpr_32__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 0, v0)) */
#include <cstdint>
#include <cstring>
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

extern "C"
uint64_t
emu_movd_xmm_gpr_32__reg_rdi__cpp(float a)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)f32_to_bits(a))));
}
