/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of fcvt_d_s_fpr_fpr_fpr_64__freg_fa0__c__native_first.  The term's text, LITERAL:
   fp.to_ieee_bv(fpToFP(RNE(), fpToFP(Extract(31, 0, v0)))) */
#include <stdint.h>
#include <string.h>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

uint64_t
emu_fcvt_d_s_fpr_fpr_fpr_64__freg_fa0__c__native_first(uint32_t a)
{
    uint32_t v0 = (uint32_t)a;
    float v1 = bits_to_f32((uint32_t)(v0));
    double v2 = ((double)(v1));
    uint64_t v3 = (uint64_t)f64_to_bits(v2);
    return (uint64_t)(v3);
}
