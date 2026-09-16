/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of SHA512SUM1R__one__rd__cpp__native_first.  The term's text, LITERAL:
    */
#include <cstdint>

extern "C"
uint64_t
emu_SHA512SUM1R__one__rd__cpp__native_first(uint64_t a, uint64_t b)
{
    uint32_t v0 = ((uint32_t)((uint64_t)a >> 18) & UINT32_C(0x3fff));
    uint32_t v1 = ((uint32_t)((uint64_t)a >> 14) & UINT32_C(0x3fff));
    uint32_t v2 = ((uint32_t)((uint64_t)b >> 9) & UINT32_C(0x3fff));
    uint32_t v3 = ((uint32_t)((uint32_t)(v2) ^ (uint32_t)(v1) ^ (uint32_t)(v0)) & UINT32_C(0x3fff));
    uint32_t v4 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0xf));
    uint32_t v5 = ((uint32_t)((uint64_t)a >> 28) & UINT32_C(0xf));
    uint32_t v6 = ((uint32_t)((uint64_t)b >> 0) & UINT32_C(0xf));
    uint32_t v7 = ((uint32_t)((uint64_t)b >> 23) & UINT32_C(0xf));
    uint32_t v8 = ((uint32_t)((uint32_t)(v7) ^ (uint32_t)(v6) ^ (uint32_t)(v5) ^ (uint32_t)(v4)) & UINT32_C(0xf));
    uint32_t v9 = ((uint32_t)((uint64_t)b >> 4) & UINT32_C(0x1f));
    uint32_t v10 = ((uint32_t)((uint64_t)a >> 36) & UINT32_C(0x1f));
    uint32_t v11 = ((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x1f));
    uint32_t v12 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0x1f));
    uint32_t v13 = ((uint32_t)((uint64_t)b >> 27) & UINT32_C(0x1f));
    uint32_t v14 = ((uint32_t)((uint32_t)(v13) ^ (uint32_t)(v12) ^ (uint32_t)(v11) ^ (uint32_t)(v10) ^ (uint32_t)(v9)) & UINT32_C(0x1f));
    uint32_t v15 = ((uint32_t)((uint64_t)a >> 41) & UINT32_C(0x7fffff));
    uint32_t v16 = ((uint32_t)((uint64_t)a >> 37) & UINT32_C(0x7fffff));
    uint32_t v17 = ((uint32_t)((uint64_t)b >> 32) & UINT32_C(0x7fffff));
    uint32_t v18 = ((uint32_t)((uint64_t)b >> 9) & UINT32_C(0x7fffff));
    uint32_t v19 = ((uint32_t)((uint64_t)b >> 5) & UINT32_C(0x7fffff));
    uint32_t v20 = ((uint32_t)((uint64_t)a >> 0) & UINT32_C(0x7fffff));
    uint32_t v21 = ((uint32_t)((uint32_t)(v20) ^ (uint32_t)(v19) ^ (uint32_t)(v18) ^ (uint32_t)(v17) ^ (uint32_t)(v16) ^ (uint32_t)(v15)) & UINT32_C(0x7fffff));
    uint32_t v22 = ((uint32_t)((uint64_t)a >> 60) & UINT32_C(0xf));
    uint32_t v23 = ((uint32_t)((uint64_t)b >> 55) & UINT32_C(0xf));
    uint32_t v24 = ((uint32_t)((uint64_t)b >> 32) & UINT32_C(0xf));
    uint32_t v25 = ((uint32_t)((uint64_t)b >> 28) & UINT32_C(0xf));
    uint32_t v26 = ((uint32_t)((uint64_t)a >> 23) & UINT32_C(0xf));
    uint32_t v27 = ((uint32_t)((uint32_t)(v26) ^ (uint32_t)(v25) ^ (uint32_t)(v24) ^ (uint32_t)(v23) ^ (uint32_t)(v22)) & UINT32_C(0xf));
    uint32_t v28 = ((uint32_t)((uint64_t)b >> 59) & UINT32_C(0x1f));
    uint32_t v29 = ((uint32_t)((uint64_t)b >> 36) & UINT32_C(0x1f));
    uint32_t v30 = ((uint32_t)((uint64_t)b >> 32) & UINT32_C(0x1f));
    uint32_t v31 = ((uint32_t)((uint64_t)a >> 27) & UINT32_C(0x1f));
    uint32_t v32 = ((uint32_t)((uint32_t)(v31) ^ (uint32_t)(v30) ^ (uint32_t)(v29) ^ (uint32_t)(v28)) & UINT32_C(0x1f));
    uint32_t v33 = ((uint32_t)((uint64_t)b >> 41) & UINT32_C(0x1ff));
    uint32_t v34 = ((uint32_t)((uint64_t)b >> 37) & UINT32_C(0x1ff));
    uint32_t v35 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0x1ff));
    uint32_t v36 = ((uint32_t)((uint32_t)(v35) ^ (uint32_t)(v34) ^ (uint32_t)(v33)) & UINT32_C(0x1ff));
    uint64_t v37 = (uint64_t)(((uint64_t)(v36) << 55) | ((uint64_t)(v32) << 50) | ((uint64_t)(v27) << 46) | ((uint64_t)(v21) << 23) | ((uint64_t)(v14) << 18) | ((uint64_t)(v8) << 14) | (uint64_t)(v3));
    return (uint64_t)(v37);
}
