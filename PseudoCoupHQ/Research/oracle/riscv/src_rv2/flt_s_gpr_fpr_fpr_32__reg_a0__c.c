/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of flt_s_gpr_fpr_fpr_32__reg_a0__c.  The term's layer-5 text, LITERAL:
   If(fpToFP(Extract(31, 0, v0)) < fpToFP(Extract(31, 0, v1)), 1, 0) */
#include <stdint.h>
#include <string.h>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }

uint64_t
emu_flt_s_gpr_fpr_fpr_32__reg_a0__c(uint32_t a, uint32_t b)
{
    return (uint64_t)(((((bits_to_f32((uint32_t)((uint32_t)a))) < (bits_to_f32((uint32_t)((uint32_t)b))))) ? (uint64_t)(UINT64_C(0x1)) : (uint64_t)(UINT64_C(0x0))));
}
