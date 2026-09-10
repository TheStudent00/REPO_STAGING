/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of fsub_d_fpr_fpr_fpr_64__freg_fa0__c.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(-fpToFP(v0) + fpToFP(v1)) */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

uint64_t
emu_fsub_d_fpr_fpr_fpr_64__freg_fa0__c(uint64_t a, uint64_t b)
{
    return (uint64_t)((uint64_t)f64_to_bits(((double)(((-(bits_to_f64((uint64_t)((uint64_t)b))))) + (bits_to_f64((uint64_t)((uint64_t)a)))))));
}
