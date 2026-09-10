/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of fcvt_s_d_fpr_fpr_32__freg_fa0__c.  The term's layer-5 text, LITERAL:
   Concat(4294967295, fp.to_ieee_bv(fpToFP(RNE(), fpToFP(v0)))) */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

uint64_t
emu_fcvt_s_d_fpr_fpr_32__freg_fa0__c(uint64_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0xffffffff)) << 32) | (uint64_t)((uint32_t)f32_to_bits(((float)(bits_to_f64((uint64_t)((uint64_t)a))))))));
}
