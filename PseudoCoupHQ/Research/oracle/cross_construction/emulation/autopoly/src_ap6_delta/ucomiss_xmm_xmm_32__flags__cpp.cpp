/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of ucomiss_xmm_xmm_32__flags__cpp.  The term's layer-5 text, LITERAL:
   Concat(fp.to_ieee_bv(fpToFP(Extract(31, 0, v0))), fp.to_ieee_bv(fpToFP(Extract(31, 0, v1)))) */
#include <cstdint>
#include <cstring>
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

extern "C"
uint64_t
emu_ucomiss_xmm_xmm_32__flags__cpp(float a, float b)
{
    return (uint64_t)((uint64_t)(((uint64_t)((uint32_t)f32_to_bits(a)) << 32) | (uint64_t)((uint32_t)f32_to_bits(b))));
}
