/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of fcvt_s_lu_fpr_gpr_32__freg_fa0__c__native_first.  The term's text, LITERAL:
   Concat(4294967295, fp.to_ieee_bv(fpToFPUnsigned(RNE(), v0))) */
#include <stdint.h>
#include <string.h>
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

uint64_t
emu_fcvt_s_lu_fpr_gpr_32__freg_fa0__c__native_first(uint64_t a)
{
    float v0 = ((float)(uint64_t)((uint64_t)a));
    uint32_t v1 = (uint32_t)f32_to_bits(v0);
    uint64_t v2 = (uint64_t)(((uint64_t)(UINT32_C(0xffffffff)) << 32) | (uint64_t)(v1));
    return (uint64_t)(v2);
}
