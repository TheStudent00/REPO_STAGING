/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of cmpneqss_mem_xmm_32__reg_xmm0__cpp.  The term's layer-5 text, LITERAL:
   If(And(fpEQ(fpToFP(Extract(31, 0, v0)), fpToFP(Extract(31, 0, v1))), Not(Or(fpIsNaN(fpToFP(Extract(31, 0, v0))), fpIsNaN(fpToFP(Extract(31, 0, v1)))))), 0, 4294967295) */
#include <cstdint>
#include <cstring>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }

extern "C"
float
emu_cmpneqss_mem_xmm_32__reg_xmm0__cpp(uint32_t a, float b)
{
    return bits_to_f32((uint32_t)(((((((b) == (bits_to_f32((uint32_t)((uint32_t)a))))) && ((!(((((b) != (b))) || (((bits_to_f32((uint32_t)((uint32_t)a))) != (bits_to_f32((uint32_t)((uint32_t)a))))))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0xffffffff)))));
}
