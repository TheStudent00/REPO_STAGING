/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of fcvt_s_wu_fpr_gpr_32__freg_fa0__c.  The term's layer-5 text, LITERAL:
   Concat(4294967295, fp.to_ieee_bv(fpToFPUnsigned(RNE(), Extract(31, 0, v0)))) */
#include <stdint.h>
#include <string.h>
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

uint64_t
emu_fcvt_s_wu_fpr_gpr_32__freg_fa0__c(uint32_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0xffffffff)) << 32) | (uint64_t)((uint32_t)f32_to_bits(((float)(uint32_t)((uint32_t)a))))));
}
