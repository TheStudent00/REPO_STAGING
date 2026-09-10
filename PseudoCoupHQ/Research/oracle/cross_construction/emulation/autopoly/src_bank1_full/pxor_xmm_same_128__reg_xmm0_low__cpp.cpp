/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of pxor_xmm_same_128__reg_xmm0_low__cpp.  The term's layer-5 text, LITERAL:
   0 */
#include <cstdint>
#include <cstring>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }

extern "C"
double
emu_pxor_xmm_same_128__reg_xmm0_low__cpp(void)
{
    return bits_to_f64((uint64_t)(UINT64_C(0x0)));
}
