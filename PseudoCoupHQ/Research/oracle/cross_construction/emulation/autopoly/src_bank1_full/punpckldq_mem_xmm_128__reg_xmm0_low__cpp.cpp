/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of punpckldq_mem_xmm_128__reg_xmm0_low__cpp.  The term's layer-5 text, LITERAL:
   Concat(Extract(31, 0, v0), Extract(31, 0, v1)) */
#include <cstdint>
#include <cstring>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

extern "C"
double
emu_punpckldq_mem_xmm_128__reg_xmm0_low__cpp(uint32_t a, float b)
{
    return bits_to_f64((uint64_t)((uint64_t)(((uint64_t)((uint32_t)a) << 32) | (uint64_t)((uint32_t)f32_to_bits(b)))));
}
