/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of fcvt_s_d_fpr_fpr_32__freg_fa0__cpp__native_first.  The term's text, LITERAL:
   Concat(4294967295, fp.to_ieee_bv(fpToFP(RNE(), fpToFP(v0)))) */
#include <cstdint>
#include <cstring>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

extern "C"
uint64_t
emu_fcvt_s_d_fpr_fpr_32__freg_fa0__cpp__native_first(uint64_t a)
{
    double v0 = bits_to_f64((uint64_t)((uint64_t)a));
    float v1 = ((float)(v0));
    uint32_t v2 = (uint32_t)f32_to_bits(v1);
    uint64_t v3 = (uint64_t)(((uint64_t)(UINT32_C(0xffffffff)) << 32) | (uint64_t)(v2));
    return (uint64_t)(v3);
}
