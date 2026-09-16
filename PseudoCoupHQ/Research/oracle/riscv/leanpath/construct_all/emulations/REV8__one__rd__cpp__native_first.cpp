/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of REV8__one__rd__cpp__native_first.  The term's text, LITERAL:
    */
#include <cstdint>

extern "C"
uint64_t
emu_REV8__one__rd__cpp__native_first(uint64_t a)
{
    uint32_t v0 = ((uint32_t)((uint64_t)a >> 56) & UINT32_C(0xff));
    uint32_t v1 = ((uint32_t)((uint64_t)a >> 48) & UINT32_C(0xff));
    uint32_t v2 = ((uint32_t)((uint64_t)a >> 40) & UINT32_C(0xff));
    uint32_t v3 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0xff));
    uint32_t v4 = ((uint32_t)((uint64_t)a >> 24) & UINT32_C(0xff));
    uint32_t v5 = ((uint32_t)((uint64_t)a >> 16) & UINT32_C(0xff));
    uint32_t v6 = ((uint32_t)((uint64_t)a >> 8) & UINT32_C(0xff));
    uint32_t v7 = ((uint32_t)((uint64_t)a >> 0) & UINT32_C(0xff));
    uint64_t v8 = (uint64_t)(((uint64_t)(v7) << 56) | ((uint64_t)(v6) << 48) | ((uint64_t)(v5) << 40) | ((uint64_t)(v4) << 32) | ((uint64_t)(v3) << 24) | ((uint64_t)(v2) << 16) | ((uint64_t)(v1) << 8) | (uint64_t)(v0));
    return (uint64_t)(v8);
}
