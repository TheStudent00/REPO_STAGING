/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of fmv_w_x_fpr_gpr_32__freg_fa0__cpp__native_first.  The term's text, LITERAL:
   Concat(4294967295, Extract(31, 0, v0)) */
#include <cstdint>

extern "C"
uint64_t
emu_fmv_w_x_fpr_gpr_32__freg_fa0__cpp__native_first(uint32_t a)
{
    uint32_t v0 = (uint32_t)a;
    uint64_t v1 = (uint64_t)(((uint64_t)(UINT32_C(0xffffffff)) << 32) | (uint64_t)(v0));
    return (uint64_t)(v1);
}
