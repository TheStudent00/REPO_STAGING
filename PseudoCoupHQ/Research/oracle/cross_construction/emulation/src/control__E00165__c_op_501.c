/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of control__E00165__c_op_501.  The term's layer-5 text, LITERAL:
   Concat(0, If(And(fpEQ(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0)))), fpToFP(Extract(31, 0, v1))), Not(Or(fpIsNaN(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0))))), fpIsNaN(fpToFP(Extract(31, 0, v1)))))), 0, 1)) */
#include <stdint.h>
#include <string.h>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

uint32_t
emu_control__E00165__c_op_501(uint32_t a, float b, double c)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 1) | (uint32_t)(((((((b) == (bits_to_f32((uint32_t)((uint32_t)f32_to_bits(((float)(int32_t)((uint32_t)a)))))))) && ((!(((((b) != (b))) || (((bits_to_f32((uint32_t)((uint32_t)f32_to_bits(((float)(int32_t)((uint32_t)a)))))) != (bits_to_f32((uint32_t)((uint32_t)f32_to_bits(((float)(int32_t)((uint32_t)a)))))))))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1))))));
}
