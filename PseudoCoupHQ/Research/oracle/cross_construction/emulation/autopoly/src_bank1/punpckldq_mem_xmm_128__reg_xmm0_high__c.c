/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of punpckldq_mem_xmm_128__reg_xmm0_high__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 32, v0), Extract(63, 32, v1)) */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

double
emu_punpckldq_mem_xmm_128__reg_xmm0_high__c(uint64_t a, double b)
{
    return bits_to_f64((uint64_t)((uint64_t)(((uint64_t)((uint32_t)((uint64_t)a >> 32)) << 32) | (uint64_t)((uint32_t)((uint64_t)f64_to_bits(b) >> 32)))));
}
