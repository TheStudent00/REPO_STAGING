/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of divss_mem_xmm_32__reg_xmm0__c.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) / fpToFP(Extract(31, 0, v1))) */
#include <stdint.h>
#include <string.h>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

float
emu_divss_mem_xmm_32__reg_xmm0__c(uint32_t a, float b)
{
    return bits_to_f32((uint32_t)((uint32_t)f32_to_bits(((float)((b) / (bits_to_f32((uint32_t)((uint32_t)a))))))));
}
