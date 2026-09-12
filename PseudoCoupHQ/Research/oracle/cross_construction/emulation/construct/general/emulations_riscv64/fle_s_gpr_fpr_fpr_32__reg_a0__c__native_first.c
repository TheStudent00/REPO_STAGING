/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of fle_s_gpr_fpr_fpr_32__reg_a0__c__native_first.  The term's text, LITERAL:
   If(fpToFP(Extract(31, 0, v0)) <= fpToFP(Extract(31, 0, v1)), 1, 0) */
#include <stdint.h>
#include <string.h>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }

uint64_t
emu_fle_s_gpr_fpr_fpr_32__reg_a0__c__native_first(uint32_t a, uint32_t b)
{
    uint32_t v0 = (uint32_t)b;
    float v1 = bits_to_f32((uint32_t)(v0));
    uint32_t v2 = (uint32_t)a;
    float v3 = bits_to_f32((uint32_t)(v2));
    int v4 = (((v3) <= (v1))) ? 1 : 0;
    uint64_t v5 = ((v4) ? (uint64_t)(UINT64_C(0x1)) : (uint64_t)(UINT64_C(0x0)));
    return (uint64_t)(v5);
}
