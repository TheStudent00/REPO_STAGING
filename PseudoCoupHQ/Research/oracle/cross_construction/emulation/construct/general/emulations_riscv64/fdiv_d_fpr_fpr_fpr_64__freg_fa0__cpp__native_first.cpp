/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of fdiv_d_fpr_fpr_fpr_64__freg_fa0__cpp__native_first.  The term's text, LITERAL:
   fp.to_ieee_bv(fpToFP(v0) / fpToFP(v1)) */
#include <cstdint>
#include <cstring>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

extern "C"
uint64_t
emu_fdiv_d_fpr_fpr_fpr_64__freg_fa0__cpp__native_first(uint64_t a, uint64_t b)
{
    double v0 = bits_to_f64((uint64_t)((uint64_t)b));
    double v1 = bits_to_f64((uint64_t)((uint64_t)a));
    double v2 = ((double)((v1) / (v0)));
    uint64_t v3 = (uint64_t)f64_to_bits(v2);
    return (uint64_t)(v3);
}
