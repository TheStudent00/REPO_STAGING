/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of SHA512SUM0R__one__rd__cpp__native_first.  The term's text, LITERAL:
    */
#include <cstdint>

extern "C"
uint64_t
emu_SHA512SUM0R__one__rd__cpp__native_first(uint64_t a, uint64_t b)
{
    uint32_t v0 = ((uint32_t)((uint64_t)b >> 2) & UINT32_C(0xf));
    uint32_t v1 = ((uint32_t)((uint64_t)a >> 28) & UINT32_C(0xf));
    uint32_t v2 = ((uint32_t)((uint64_t)b >> 7) & UINT32_C(0xf));
    uint32_t v3 = ((uint32_t)((uint32_t)(v2) ^ (uint32_t)(v1) ^ (uint32_t)(v0)) & UINT32_C(0xf));
    uint32_t v4 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0x1fffff));
    uint32_t v5 = ((uint32_t)((uint64_t)b >> 11) & UINT32_C(0x1fffff));
    uint32_t v6 = ((uint32_t)((uint64_t)b >> 6) & UINT32_C(0x1fffff));
    uint32_t v7 = ((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x1fffff));
    uint32_t v8 = ((uint32_t)((uint32_t)(v7) ^ (uint32_t)(v6) ^ (uint32_t)(v5) ^ (uint32_t)(v4)) & UINT32_C(0x1fffff));
    uint32_t v9 = ((uint32_t)((uint64_t)a >> 53) & UINT32_C(0x1f));
    uint32_t v10 = ((uint32_t)((uint64_t)a >> 0) & UINT32_C(0x1f));
    uint32_t v11 = ((uint32_t)((uint64_t)b >> 32) & UINT32_C(0x1f));
    uint32_t v12 = ((uint32_t)((uint64_t)b >> 27) & UINT32_C(0x1f));
    uint32_t v13 = ((uint32_t)((uint64_t)b >> 21) & UINT32_C(0x1f));
    uint32_t v14 = ((uint32_t)((uint32_t)(v13) ^ (uint32_t)(v12) ^ (uint32_t)(v11) ^ (uint32_t)(v10) ^ (uint32_t)(v9)) & UINT32_C(0x1f));
    uint32_t v15 = ((uint32_t)((uint64_t)a >> 58) & UINT32_C(0x3f));
    uint32_t v16 = ((uint32_t)((uint64_t)a >> 0) & UINT32_C(0x3f));
    uint32_t v17 = ((uint32_t)((uint64_t)b >> 37) & UINT32_C(0x3f));
    uint32_t v18 = ((uint32_t)((uint64_t)b >> 32) & UINT32_C(0x3f));
    uint32_t v19 = ((uint32_t)((uint64_t)b >> 26) & UINT32_C(0x3f));
    uint32_t v20 = ((uint32_t)((uint64_t)a >> 5) & UINT32_C(0x3f));
    uint32_t v21 = ((uint32_t)((uint32_t)(v20) ^ (uint32_t)(v19) ^ (uint32_t)(v18) ^ (uint32_t)(v17) ^ (uint32_t)(v16) ^ (uint32_t)(v15)) & UINT32_C(0x3f));
    uint32_t v22 = ((uint32_t)((uint64_t)b >> 43) & UINT32_C(0x1fffff));
    uint32_t v23 = ((uint32_t)((uint64_t)b >> 38) & UINT32_C(0x1fffff));
    uint32_t v24 = ((uint32_t)((uint64_t)b >> 32) & UINT32_C(0x1fffff));
    uint32_t v25 = ((uint32_t)((uint64_t)a >> 11) & UINT32_C(0x1fffff));
    uint32_t v26 = ((uint32_t)((uint64_t)a >> 6) & UINT32_C(0x1fffff));
    uint32_t v27 = ((uint32_t)((uint32_t)(v26) ^ (uint32_t)(v25) ^ (uint32_t)(v24) ^ (uint32_t)(v23) ^ (uint32_t)(v22)) & UINT32_C(0x1fffff));
    uint32_t v28 = ((uint32_t)((uint64_t)b >> 59) & UINT32_C(0x1f));
    uint32_t v29 = ((uint32_t)((uint64_t)b >> 53) & UINT32_C(0x1f));
    uint32_t v30 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0x1f));
    uint32_t v31 = ((uint32_t)((uint64_t)a >> 27) & UINT32_C(0x1f));
    uint32_t v32 = ((uint32_t)((uint32_t)(v31) ^ (uint32_t)(v30) ^ (uint32_t)(v29) ^ (uint32_t)(v28)) & UINT32_C(0x1f));
    uint32_t v33 = ((uint32_t)((uint64_t)b >> 58) & UINT32_C(0x3));
    uint32_t v34 = ((uint32_t)((uint64_t)a >> 37) & UINT32_C(0x3));
    uint32_t v35 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0x3));
    uint32_t v36 = ((uint32_t)((uint32_t)(v35) ^ (uint32_t)(v34) ^ (uint32_t)(v33)) & UINT32_C(0x3));
    uint64_t v37 = (uint64_t)(((uint64_t)(v36) << 62) | ((uint64_t)(v32) << 57) | ((uint64_t)(v27) << 36) | ((uint64_t)(v21) << 30) | ((uint64_t)(v14) << 25) | ((uint64_t)(v8) << 4) | (uint64_t)(v3));
    return (uint64_t)(v37);
}
