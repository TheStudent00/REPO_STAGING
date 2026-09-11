/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of ucomisd_xmm_xmm_64__flags_high__c__native_first.  The term's text, LITERAL:
   fp.to_ieee_bv(fpToFP(Extract(63, 0, v0))) */
#include <stdint.h>
#include <string.h>
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

uint64_t
emu_ucomisd_xmm_xmm_64__flags_high__c__native_first(double a)
{
    double v1 = a;
    uint64_t v2 = (uint64_t)f64_to_bits(v1);
    return (uint64_t)(v2);
}
