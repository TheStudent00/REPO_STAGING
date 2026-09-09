/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of xorpd_xmm_same_128__reg_xmm0_high__c.  The term's layer-5 text, LITERAL:
   0 */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }

double
emu_xorpd_xmm_same_128__reg_xmm0_high__c(void)
{
    return bits_to_f64((uint64_t)(UINT64_C(0x0)));
}
