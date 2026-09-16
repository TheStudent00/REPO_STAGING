/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of ZBS_IOP__op_BINVI__rd__cpp__native_first.  The term's text, LITERAL:
    */
#include <cstdint>

extern "C"
uint64_t
emu_ZBS_IOP__op_BINVI__rd__cpp__native_first(uint64_t a, uint8_t b)
{
    uint32_t v0 = ((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x3f));
    uint64_t v1 = (uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(v0));
    uint64_t v2 = (uint64_t)((uint64_t)(UINT64_C(0x1)) << (unsigned)(uint64_t)(v1));
    uint64_t v3 = (uint64_t)((uint64_t)(v2) ^ (uint64_t)((uint64_t)a));
    return (uint64_t)(v3);
}
