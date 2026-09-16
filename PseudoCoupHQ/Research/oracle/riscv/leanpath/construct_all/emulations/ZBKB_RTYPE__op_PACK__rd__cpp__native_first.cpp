/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of ZBKB_RTYPE__op_PACK__rd__cpp__native_first.  The term's text, LITERAL:
    */
#include <cstdint>

extern "C"
uint64_t
emu_ZBKB_RTYPE__op_PACK__rd__cpp__native_first(uint32_t a, uint32_t b)
{
    uint32_t v0 = (uint32_t)b;
    uint32_t v1 = (uint32_t)a;
    uint64_t v2 = (uint64_t)(((uint64_t)(v1) << 32) | (uint64_t)(v0));
    return (uint64_t)(v2);
}
