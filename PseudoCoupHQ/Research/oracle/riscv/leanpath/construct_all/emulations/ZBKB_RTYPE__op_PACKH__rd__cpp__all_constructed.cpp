/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of ZBKB_RTYPE__op_PACKH__rd__cpp__all_constructed.  The term's text, LITERAL:
    */
#include <cstdint>

extern "C"
uint64_t
emu_ZBKB_RTYPE__op_PACKH__rd__cpp__all_constructed(uint8_t a, uint8_t b)
{
    uint32_t v0 = (uint32_t)b;
    uint32_t v1 = (uint32_t)a;
    uint32_t v2 = v0;
    uint32_t v3 = v1;
    uint64_t v4 = UINT64_C(0x0);
    uint64_t v5 = ((uint64_t)(((uint64_t)(v4) << 8) | (uint64_t)(v3)) & UINT64_C(0xffffffffffffff));
    uint64_t v6 = (uint64_t)(((uint64_t)(v5) << 8) | (uint64_t)(v2));
    return (uint64_t)(v6);
}
