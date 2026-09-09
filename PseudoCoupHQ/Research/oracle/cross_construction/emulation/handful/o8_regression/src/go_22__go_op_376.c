/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of go_22__go_op_376.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(-fpToFP(Extract(63, 0, v0)) + fpToFP(Extract(63, 0, v1))) */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

double
emu_go_22__go_op_376(double a, double b)
{
    return bits_to_f64((uint64_t)((uint64_t)f64_to_bits(((double)(((-(b))) + (a))))));
}
