/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of bge_gpr_gpr_gpr_64__branch_condition__cpp__native_first.  The term's text, LITERAL:
   If(v0 <= v1, 1, 0) */
#include <cstdint>

extern "C"
uint64_t
emu_bge_gpr_gpr_gpr_64__branch_condition__cpp__native_first(uint64_t a, uint64_t b)
{
    int v0 = (((int64_t)((uint64_t)b) <= (int64_t)((uint64_t)a))) ? 1 : 0;
    uint64_t v1 = ((v0) ? (uint64_t)(UINT64_C(0x1)) : (uint64_t)(UINT64_C(0x0)));
    return (uint64_t)(v1);
}
