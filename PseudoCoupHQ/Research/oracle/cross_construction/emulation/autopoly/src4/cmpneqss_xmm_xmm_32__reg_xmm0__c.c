/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of cmpneqss_xmm_xmm_32__reg_xmm0__c.  The term's layer-5 text, LITERAL:
   If(And(fpEQ(fpToFP(Extract(31, 0, v0)), fpToFP(Extract(31, 0, v1))), Not(Or(fpIsNaN(fpToFP(Extract(31, 0, v0))), fpIsNaN(fpToFP(Extract(31, 0, v1)))))), 0, 4294967295) */
#include <stdint.h>
#include <string.h>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }

float
emu_cmpneqss_xmm_xmm_32__reg_xmm0__c(float a, float b)
{
    return bits_to_f32((uint32_t)(((((((a) == (b))) && ((!(((((a) != (a))) || (((b) != (b))))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0xffffffff)))));
}
