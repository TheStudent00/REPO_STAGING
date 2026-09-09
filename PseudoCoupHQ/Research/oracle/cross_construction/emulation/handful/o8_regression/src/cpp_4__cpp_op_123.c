/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of cpp_4__cpp_op_123.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))) */
#include <stdint.h>
#include <string.h>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

float
emu_cpp_4__cpp_op_123(double a, float b)
{
    return bits_to_f32((uint32_t)((uint64_t)(((uint64_t)((uint32_t)((uint64_t)f64_to_bits(a) >> 32)) << 32) | (uint64_t)((uint32_t)f32_to_bits(((float)((bits_to_f32((uint32_t)((uint32_t)((uint64_t)f64_to_bits(a) >> 0)))) + (b))))))));
}
