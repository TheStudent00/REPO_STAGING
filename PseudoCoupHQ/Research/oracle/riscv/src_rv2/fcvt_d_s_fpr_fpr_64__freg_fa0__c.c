/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of fcvt_d_s_fpr_fpr_64__freg_fa0__c.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(fpToFP(RNE(), fpToFP(Extract(31, 0, v0)))) */
#include <stdint.h>
#include <string.h>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

uint64_t
emu_fcvt_d_s_fpr_fpr_64__freg_fa0__c(uint32_t a)
{
    return (uint64_t)((uint64_t)f64_to_bits(((double)(bits_to_f32((uint32_t)((uint32_t)a))))));
}
