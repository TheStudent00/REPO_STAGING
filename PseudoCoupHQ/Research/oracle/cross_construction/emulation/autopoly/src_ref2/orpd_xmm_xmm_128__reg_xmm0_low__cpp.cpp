/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of orpd_xmm_xmm_128__reg_xmm0_low__cpp.  The term's layer-5 text, LITERAL:
   Extract(63, 0, v0) | Extract(63, 0, v1) */
#include <cstdint>
#include <cstring>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

extern "C"
double
emu_orpd_xmm_xmm_128__reg_xmm0_low__cpp(double a, double b)
{
    return bits_to_f64((uint64_t)((uint64_t)((uint64_t)((uint64_t)f64_to_bits(a)) | (uint64_t)((uint64_t)f64_to_bits(b)))));
}
