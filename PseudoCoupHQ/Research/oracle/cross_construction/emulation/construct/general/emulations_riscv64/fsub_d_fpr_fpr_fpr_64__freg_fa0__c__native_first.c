/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of fsub_d_fpr_fpr_fpr_64__freg_fa0__c__native_first.  The term's text, LITERAL:
   fp.to_ieee_bv(-fpToFP(v0) + fpToFP(v1)) */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

uint64_t
emu_fsub_d_fpr_fpr_fpr_64__freg_fa0__c__native_first(uint64_t a, uint64_t b)
{
    double v0 = bits_to_f64((uint64_t)((uint64_t)a));
    double v1 = bits_to_f64((uint64_t)((uint64_t)b));
    double v2 = (-(v1));
    double v3 = ((double)((v2) + (v0)));
    uint64_t v4 = (uint64_t)f64_to_bits(v3);
    return (uint64_t)(v4);
}
