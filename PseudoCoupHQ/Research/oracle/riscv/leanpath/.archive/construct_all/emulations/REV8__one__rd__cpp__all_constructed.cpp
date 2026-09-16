/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of REV8__one__rd__cpp__all_constructed.  The term's text, LITERAL:
    */
#include <cstdint>

extern "C"
uint64_t
emu_REV8__one__rd__cpp__all_constructed(uint64_t a)
{
    uint32_t v0 = ((uint32_t)((uint64_t)a >> 56) & UINT32_C(0xff));
    uint32_t v1 = ((uint32_t)((uint64_t)a >> 48) & UINT32_C(0xff));
    uint32_t v2 = ((uint32_t)((uint64_t)a >> 40) & UINT32_C(0xff));
    uint32_t v3 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0xff));
    uint32_t v4 = ((uint32_t)((uint64_t)a >> 24) & UINT32_C(0xff));
    uint32_t v5 = ((uint32_t)((uint64_t)a >> 16) & UINT32_C(0xff));
    uint32_t v6 = ((uint32_t)((uint64_t)a >> 8) & UINT32_C(0xff));
    uint32_t v7 = ((uint32_t)((uint64_t)a >> 0) & UINT32_C(0xff));
    uint32_t v8 = v0;
    uint32_t v9 = v1;
    uint32_t v10 = v2;
    uint32_t v11 = v3;
    uint32_t v12 = v4;
    uint32_t v13 = v5;
    uint32_t v14 = v6;
    uint32_t v15 = v7;
    uint32_t v16 = ((uint32_t)(((uint32_t)(v15) << 8) | (uint32_t)(v14)) & UINT32_C(0xffff));
    uint32_t v17 = ((uint32_t)(((uint32_t)(v16) << 8) | (uint32_t)(v13)) & UINT32_C(0xffffff));
    uint32_t v18 = (uint32_t)(((uint32_t)(v17) << 8) | (uint32_t)(v12));
    uint64_t v19 = ((uint64_t)(((uint64_t)(v18) << 8) | (uint64_t)(v11)) & UINT64_C(0xffffffffff));
    uint64_t v20 = ((uint64_t)(((uint64_t)(v19) << 8) | (uint64_t)(v10)) & UINT64_C(0xffffffffffff));
    uint64_t v21 = ((uint64_t)(((uint64_t)(v20) << 8) | (uint64_t)(v9)) & UINT64_C(0xffffffffffffff));
    uint64_t v22 = (uint64_t)(((uint64_t)(v21) << 8) | (uint64_t)(v8));
    return (uint64_t)(v22);
}
