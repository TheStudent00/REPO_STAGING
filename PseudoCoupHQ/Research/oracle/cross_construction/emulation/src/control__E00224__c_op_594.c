/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of control__E00224__c_op_594.  The term's layer-5 text, LITERAL:
   If(And(Not(fpToFP(Extract(63, 0, v1)) < fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0))))), Not(Or(fpIsNaN(fpToFP(Extract(63, 0, v1))), fpIsNaN(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0)))))))), 1, 0) */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

uint8_t
emu_control__E00224__c_op_594(uint32_t a, double b, double c)
{
    return (uint8_t)((((((!(((b) < (bits_to_f64((uint64_t)((uint64_t)f64_to_bits(((double)(int32_t)((uint32_t)a)))))))))) && ((!(((((b) != (b))) || (((bits_to_f64((uint64_t)((uint64_t)f64_to_bits(((double)(int32_t)((uint32_t)a)))))) != (bits_to_f64((uint64_t)((uint64_t)f64_to_bits(((double)(int32_t)((uint32_t)a)))))))))))))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0))));
}
