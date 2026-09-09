/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of control__E00422__c_regen_8743.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(fpToFP(Extract(63, 0, v1)) * fpToFP(fp.to_ieee_bv(fpToFP(RNE(), fpToFP(Concat(Extract(15, 0, v0), 0)))))) */
#include <stdint.h>
#include <string.h>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint16_t f16_to_bits(_Float16 f) { uint16_t b; memcpy(&b, &f, 2); return b; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

double
emu_control__E00422__c_regen_8743(double a, _Float16 b)
{
    return bits_to_f64((uint64_t)((uint64_t)f64_to_bits(((double)((a) * (bits_to_f64((uint64_t)((uint64_t)f64_to_bits(((double)(bits_to_f32((uint32_t)((uint32_t)(((uint32_t)((uint32_t)f16_to_bits(b)) << 16) | (uint32_t)(UINT32_C(0x0))))))))))))))));
}
