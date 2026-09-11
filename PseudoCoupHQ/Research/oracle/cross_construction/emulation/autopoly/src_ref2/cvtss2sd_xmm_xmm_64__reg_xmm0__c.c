/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of cvtss2sd_xmm_xmm_64__reg_xmm0__c.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(fpToFP(RNE(), fpToFP(Extract(31, 0, v0)))) */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

double
emu_cvtss2sd_xmm_xmm_64__reg_xmm0__c(float a)
{
    return bits_to_f64((uint64_t)((uint64_t)f64_to_bits(((double)(a)))));
}
