/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of flt_d_gpr_fpr_fpr_64__reg_a0__cpp__native_first.  The term's text, LITERAL:
   If(fpToFP(v0) < fpToFP(v1), 1, 0) */
#include <cstdint>
#include <cstring>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }

extern "C"
uint64_t
emu_flt_d_gpr_fpr_fpr_64__reg_a0__cpp__native_first(uint64_t a, uint64_t b)
{
    double v0 = bits_to_f64((uint64_t)((uint64_t)b));
    double v1 = bits_to_f64((uint64_t)((uint64_t)a));
    int v2 = (((v1) < (v0))) ? 1 : 0;
    uint64_t v3 = ((v2) ? (uint64_t)(UINT64_C(0x1)) : (uint64_t)(UINT64_C(0x0)));
    return (uint64_t)(v3);
}
