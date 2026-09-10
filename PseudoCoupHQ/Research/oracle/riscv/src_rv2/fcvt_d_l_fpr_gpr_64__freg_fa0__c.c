/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of fcvt_d_l_fpr_gpr_64__freg_fa0__c.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(fpToFP(RNE(), v0)) */
#include <stdint.h>
#include <string.h>
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

uint64_t
emu_fcvt_d_l_fpr_gpr_64__freg_fa0__c(uint64_t a)
{
    return (uint64_t)((uint64_t)f64_to_bits(((double)(int64_t)((uint64_t)a))));
}
