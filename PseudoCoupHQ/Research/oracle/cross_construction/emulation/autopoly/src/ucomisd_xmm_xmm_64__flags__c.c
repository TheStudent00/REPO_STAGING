/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of ucomisd_xmm_xmm_64__flags__c.  The term's layer-5 text, LITERAL:
   Concat(fp.to_ieee_bv(fpToFP(Extract(63, 0, v0))), fp.to_ieee_bv(fpToFP(Extract(63, 0, v1)))) */
#include <stdint.h>
#include <string.h>
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

unsigned __int128
emu_ucomisd_xmm_xmm_64__flags__c(double a, double b)
{
    return (unsigned __int128)((unsigned __int128)(((unsigned __int128)((uint64_t)f64_to_bits(a)) << 64) | (unsigned __int128)((uint64_t)f64_to_bits(b))));
}
