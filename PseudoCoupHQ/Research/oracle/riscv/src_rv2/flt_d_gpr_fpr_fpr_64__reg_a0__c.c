/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of flt_d_gpr_fpr_fpr_64__reg_a0__c.  The term's layer-5 text, LITERAL:
   If(fpToFP(v0) < fpToFP(v1), 1, 0) */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }

uint64_t
emu_flt_d_gpr_fpr_fpr_64__reg_a0__c(uint64_t a, uint64_t b)
{
    return (uint64_t)(((((bits_to_f64((uint64_t)((uint64_t)a))) < (bits_to_f64((uint64_t)((uint64_t)b))))) ? (uint64_t)(UINT64_C(0x1)) : (uint64_t)(UINT64_C(0x0))));
}
