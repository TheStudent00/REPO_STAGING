/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of cmpeqsd_xmm_xmm_64__reg_xmm0__cpp.  The term's layer-5 text, LITERAL:
   If(And(fpEQ(fpToFP(Extract(63, 0, v0)), fpToFP(Extract(63, 0, v1))), Not(Or(fpIsNaN(fpToFP(Extract(63, 0, v0))), fpIsNaN(fpToFP(Extract(63, 0, v1)))))), 18446744073709551615, 0) */
#include <cstdint>
#include <cstring>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }

extern "C"
double
emu_cmpeqsd_xmm_xmm_64__reg_xmm0__cpp(double a, double b)
{
    return bits_to_f64((uint64_t)(((((((a) == (b))) && ((!(((((a) != (a))) || (((b) != (b))))))))) ? (uint64_t)(UINT64_C(0xffffffffffffffff)) : (uint64_t)(UINT64_C(0x0)))));
}
