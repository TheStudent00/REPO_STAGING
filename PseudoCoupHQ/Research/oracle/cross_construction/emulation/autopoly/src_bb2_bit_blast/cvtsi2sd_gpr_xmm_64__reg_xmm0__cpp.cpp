/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of cvtsi2sd_gpr_xmm_64__reg_xmm0__cpp.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(fpToFP(RNE(), v0)) */
#include <cstdint>
#include <cstring>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

extern "C"
double
emu_cvtsi2sd_gpr_xmm_64__reg_xmm0__cpp(uint64_t a)
{
    return bits_to_f64((uint64_t)((uint64_t)f64_to_bits(((double)(int64_t)((uint64_t)a)))));
}
