/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of ucomiss_xmm_xmm_32__flags__c__native_first.  The term's text, LITERAL:
   Concat(fp.to_ieee_bv(fpToFP(Extract(31, 0, v0))), fp.to_ieee_bv(fpToFP(Extract(31, 0, v1)))) */
#include <stdint.h>
#include <string.h>
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

uint64_t
emu_ucomiss_xmm_xmm_32__flags__c__native_first(float a, float b)
{
    float v1 = b;
    uint32_t v2 = (uint32_t)f32_to_bits(v1);
    float v4 = a;
    uint32_t v5 = (uint32_t)f32_to_bits(v4);
    uint64_t v6 = (uint64_t)(((uint64_t)(v5) << 32) | (uint64_t)(v2));
    return (uint64_t)(v6);
}
