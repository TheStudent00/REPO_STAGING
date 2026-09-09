/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of movsd_mem_xmm_64__reg_xmm0__c.  The term's layer-5 text, LITERAL:
   v0 */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }

double
emu_movsd_mem_xmm_64__reg_xmm0__c(uint64_t a)
{
    return bits_to_f64((uint64_t)((uint64_t)a));
}
