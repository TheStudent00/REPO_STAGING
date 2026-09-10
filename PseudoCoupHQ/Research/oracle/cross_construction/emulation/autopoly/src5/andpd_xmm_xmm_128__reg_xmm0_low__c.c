/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of andpd_xmm_xmm_128__reg_xmm0_low__c.  The term's layer-5 text, LITERAL:
   ~(~Extract(63, 0, v0) | ~Extract(63, 0, v1)) */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

double
emu_andpd_xmm_xmm_128__reg_xmm0_low__c(double a, double b)
{
    return bits_to_f64((uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)((uint64_t)(~(uint64_t)((uint64_t)f64_to_bits(a)))) | (uint64_t)((uint64_t)(~(uint64_t)((uint64_t)f64_to_bits(b)))))))));
}
