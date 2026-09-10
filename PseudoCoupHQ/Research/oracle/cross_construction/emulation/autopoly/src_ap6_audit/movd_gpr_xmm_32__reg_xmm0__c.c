/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of movd_gpr_xmm_32__reg_xmm0__c.  The term's layer-5 text, LITERAL:
   Extract(31, 0, v0) */
#include <stdint.h>
#include <string.h>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }

float
emu_movd_gpr_xmm_32__reg_xmm0__c(uint32_t a)
{
    return bits_to_f32((uint32_t)((uint32_t)a));
}
