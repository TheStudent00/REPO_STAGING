/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of subsd_xmm_xmm_64__reg_xmm0__c.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(-fpToFP(Extract(63, 0, v0)) + fpToFP(Extract(63, 0, v1))) */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

double
emu_subsd_xmm_xmm_64__reg_xmm0__c(double a, double b)
{
    return bits_to_f64((uint64_t)((uint64_t)f64_to_bits(((double)(((-(a))) + (b))))));
}
