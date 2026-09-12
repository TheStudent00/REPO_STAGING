/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of fadd_s_fpr_fpr_fpr_32__freg_fa0__cpp__native_first.  The term's text, LITERAL:
   Concat(4294967295, fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))) */
#include <cstdint>
#include <cstring>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

extern "C"
uint64_t
emu_fadd_s_fpr_fpr_fpr_32__freg_fa0__cpp__native_first(uint32_t a, uint32_t b)
{
    uint32_t v0 = (uint32_t)b;
    float v1 = bits_to_f32((uint32_t)(v0));
    uint32_t v2 = (uint32_t)a;
    float v3 = bits_to_f32((uint32_t)(v2));
    float v4 = ((float)((v3) + (v1)));
    uint32_t v5 = (uint32_t)f32_to_bits(v4);
    uint64_t v6 = (uint64_t)(((uint64_t)(UINT32_C(0xffffffff)) << 32) | (uint64_t)(v5));
    return (uint64_t)(v6);
}
