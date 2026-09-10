/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of divss_xmm_xmm_32__reg_xmm0__cpp.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) / fpToFP(Extract(31, 0, v1))) */
#include <cstdint>
#include <cstring>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

extern "C"
float
emu_divss_xmm_xmm_32__reg_xmm0__cpp(float a, float b)
{
    return bits_to_f32((uint32_t)((uint32_t)f32_to_bits(((float)((a) / (b))))));
}
