/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of RTYPE__op_SUB__rd__cpp__native_first.  The term's text, LITERAL:
    */
#include <cstdint>

extern "C"
uint64_t
emu_RTYPE__op_SUB__rd__cpp__native_first(uint64_t a, uint64_t b)
{
    uint64_t v0 = (uint64_t)((uint64_t)((uint64_t)b) * (uint64_t)(UINT64_C(0xffffffffffffffff)));
    uint64_t v1 = (uint64_t)((uint64_t)(v0) + (uint64_t)((uint64_t)a));
    return (uint64_t)(v1);
}
