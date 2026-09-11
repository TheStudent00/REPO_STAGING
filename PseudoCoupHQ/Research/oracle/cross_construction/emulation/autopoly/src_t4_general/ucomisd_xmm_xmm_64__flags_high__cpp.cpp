/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of ucomisd_xmm_xmm_64__flags_high__cpp.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(fpToFP(Extract(63, 0, v0))) */
#include <cstdint>
#include <cstring>
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

extern "C"
uint64_t
emu_ucomisd_xmm_xmm_64__flags_high__cpp(double a)
{
    return (uint64_t)((uint64_t)f64_to_bits(a));
}
