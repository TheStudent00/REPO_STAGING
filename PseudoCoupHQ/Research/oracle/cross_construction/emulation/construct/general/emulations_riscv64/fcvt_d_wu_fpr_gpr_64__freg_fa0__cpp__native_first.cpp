/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of fcvt_d_wu_fpr_gpr_64__freg_fa0__cpp__native_first.  The term's text, LITERAL:
   fp.to_ieee_bv(fpToFPUnsigned(RNE(), Extract(31, 0, v0))) */
#include <cstdint>
#include <cstring>
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

extern "C"
uint64_t
emu_fcvt_d_wu_fpr_gpr_64__freg_fa0__cpp__native_first(uint32_t a)
{
    uint32_t v0 = (uint32_t)a;
    double v1 = ((double)(uint32_t)(v0));
    uint64_t v2 = (uint64_t)f64_to_bits(v1);
    return (uint64_t)(v2);
}
