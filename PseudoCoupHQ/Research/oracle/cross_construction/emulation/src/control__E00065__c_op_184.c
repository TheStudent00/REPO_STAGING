/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of control__E00065__c_op_184.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(fpToFP(Extract(63, 0, v0)) * fpToFP(fp.to_ieee_bv(fpToFP(RNE(), v1)))) */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

double
emu_control__E00065__c_op_184(uint64_t a, double b, double c)
{
    return bits_to_f64((uint64_t)((uint64_t)f64_to_bits(((double)((b) * (bits_to_f64((uint64_t)((uint64_t)f64_to_bits(((double)(int64_t)((uint64_t)a)))))))))));
}
