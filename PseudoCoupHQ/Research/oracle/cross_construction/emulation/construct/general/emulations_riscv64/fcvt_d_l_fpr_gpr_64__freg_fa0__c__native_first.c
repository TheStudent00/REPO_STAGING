/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of fcvt_d_l_fpr_gpr_64__freg_fa0__c__native_first.  The term's text, LITERAL:
   fp.to_ieee_bv(fpToFP(RNE(), v0)) */
#include <stdint.h>
#include <string.h>
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

uint64_t
emu_fcvt_d_l_fpr_gpr_64__freg_fa0__c__native_first(uint64_t a)
{
    double v0 = ((double)(int64_t)((uint64_t)a));
    uint64_t v1 = (uint64_t)f64_to_bits(v0);
    return (uint64_t)(v1);
}
