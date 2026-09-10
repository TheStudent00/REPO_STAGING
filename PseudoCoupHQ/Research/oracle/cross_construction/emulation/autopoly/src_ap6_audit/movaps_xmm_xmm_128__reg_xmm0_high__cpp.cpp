/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of movaps_xmm_xmm_128__reg_xmm0_high__cpp.  The term's layer-5 text, LITERAL:
   v0 */
#include <cstdint>
#include <cstring>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }

extern "C"
double
emu_movaps_xmm_xmm_128__reg_xmm0_high__cpp(uint64_t a)
{
    return bits_to_f64((uint64_t)((uint64_t)a));
}
