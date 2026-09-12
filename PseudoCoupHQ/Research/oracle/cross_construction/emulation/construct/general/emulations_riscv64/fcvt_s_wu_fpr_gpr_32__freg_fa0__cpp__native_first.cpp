/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of fcvt_s_wu_fpr_gpr_32__freg_fa0__cpp__native_first.  The term's text, LITERAL:
   Concat(4294967295, fp.to_ieee_bv(fpToFPUnsigned(RNE(), Extract(31, 0, v0)))) */
#include <cstdint>
#include <cstring>
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

extern "C"
uint64_t
emu_fcvt_s_wu_fpr_gpr_32__freg_fa0__cpp__native_first(uint32_t a)
{
    uint32_t v0 = (uint32_t)a;
    float v1 = ((float)(uint32_t)(v0));
    uint32_t v2 = (uint32_t)f32_to_bits(v1);
    uint64_t v3 = (uint64_t)(((uint64_t)(UINT32_C(0xffffffff)) << 32) | (uint64_t)(v2));
    return (uint64_t)(v3);
}
