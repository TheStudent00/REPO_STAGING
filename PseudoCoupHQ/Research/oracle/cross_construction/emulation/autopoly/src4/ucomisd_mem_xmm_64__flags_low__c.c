/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of ucomisd_mem_xmm_64__flags_low__c.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(fpToFP(v0)) */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

uint64_t
emu_ucomisd_mem_xmm_64__flags_low__c(uint64_t a)
{
    return (uint64_t)((uint64_t)f64_to_bits(bits_to_f64((uint64_t)((uint64_t)a))));
}
