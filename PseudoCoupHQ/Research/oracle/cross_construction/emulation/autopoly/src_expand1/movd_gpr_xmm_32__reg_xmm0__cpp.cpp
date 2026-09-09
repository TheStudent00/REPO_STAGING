/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of movd_gpr_xmm_32__reg_xmm0__cpp.  The term's layer-5 text, LITERAL:
   Extract(31, 0, v0) */
#include <cstdint>
#include <cstring>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }

extern "C"
float
emu_movd_gpr_xmm_32__reg_xmm0__cpp(uint32_t a)
{
    return bits_to_f32((uint32_t)((uint32_t)a));
}
