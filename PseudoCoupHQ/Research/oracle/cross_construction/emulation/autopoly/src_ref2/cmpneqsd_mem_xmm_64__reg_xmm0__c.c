/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of cmpneqsd_mem_xmm_64__reg_xmm0__c.  The term's layer-5 text, LITERAL:
   If(And(fpEQ(fpToFP(Extract(63, 0, v0)), fpToFP(v1)), Not(Or(fpIsNaN(fpToFP(Extract(63, 0, v0))), fpIsNaN(fpToFP(v1))))), 0, 18446744073709551615) */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }

double
emu_cmpneqsd_mem_xmm_64__reg_xmm0__c(uint64_t a, double b)
{
    return bits_to_f64((uint64_t)(((((((b) == (bits_to_f64((uint64_t)((uint64_t)a))))) && ((!(((((b) != (b))) || (((bits_to_f64((uint64_t)((uint64_t)a))) != (bits_to_f64((uint64_t)((uint64_t)a))))))))))) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)(UINT64_C(0xffffffffffffffff)))));
}
