/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of ucomiss_mem_xmm_32__flags__c.  The term's layer-5 text, LITERAL:
   Concat(fp.to_ieee_bv(fpToFP(Extract(31, 0, v0))), fp.to_ieee_bv(fpToFP(Extract(31, 0, v1)))) */
#include <stdint.h>
#include <string.h>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

uint64_t
emu_ucomiss_mem_xmm_32__flags__c(uint32_t a, float b)
{
    return (uint64_t)((uint64_t)(((uint64_t)((uint32_t)f32_to_bits(b)) << 32) | (uint64_t)((uint32_t)f32_to_bits(bits_to_f32((uint32_t)((uint32_t)a))))));
}
