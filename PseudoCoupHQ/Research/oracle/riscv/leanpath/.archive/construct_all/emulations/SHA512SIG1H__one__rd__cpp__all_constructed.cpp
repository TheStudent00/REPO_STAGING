/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of SHA512SIG1H__one__rd__cpp__all_constructed.  The term's text, LITERAL:
    */
#include <cstdint>

extern "C"
uint64_t
emu_SHA512SIG1H__one__rd__cpp__all_constructed(uint64_t a, uint64_t b)
{
    uint32_t v0 = ((uint32_t)((uint64_t)a >> 6) & UINT32_C(0x7));
    uint32_t v1 = ((uint32_t)((uint64_t)b >> 29) & UINT32_C(0x7));
    uint32_t v2 = ((uint32_t)((uint64_t)a >> 19) & UINT32_C(0x7));
    uint32_t v3 = ((uint32_t)((uint32_t)(v2) ^ (uint32_t)(v1)) & UINT32_C(0x7));
    uint32_t v4 = ((uint32_t)((uint32_t)(v3) ^ (uint32_t)(v0)) & UINT32_C(0x7));
    uint32_t v5 = ((uint32_t)((uint64_t)a >> 0) & UINT32_C(0x3ff));
    uint32_t v6 = ((uint32_t)((uint64_t)b >> 32) & UINT32_C(0x3ff));
    uint32_t v7 = ((uint32_t)((uint64_t)a >> 22) & UINT32_C(0x3ff));
    uint32_t v8 = ((uint32_t)((uint64_t)a >> 9) & UINT32_C(0x3ff));
    uint32_t v9 = ((uint32_t)((uint32_t)(v8) ^ (uint32_t)(v7)) & UINT32_C(0x3ff));
    uint32_t v10 = ((uint32_t)((uint32_t)(v9) ^ (uint32_t)(v6)) & UINT32_C(0x3ff));
    uint32_t v11 = ((uint32_t)((uint32_t)(v10) ^ (uint32_t)(v5)) & UINT32_C(0x3ff));
    uint32_t v12 = ((uint32_t)((uint64_t)b >> 42) & UINT32_C(0x3fffff));
    uint32_t v13 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0x3fffff));
    uint32_t v14 = ((uint32_t)((uint64_t)a >> 19) & UINT32_C(0x3fffff));
    uint32_t v15 = ((uint32_t)((uint64_t)a >> 10) & UINT32_C(0x3fffff));
    uint32_t v16 = ((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x3fffff));
    uint32_t v17 = ((uint32_t)((uint32_t)(v16) ^ (uint32_t)(v15)) & UINT32_C(0x3fffff));
    uint32_t v18 = ((uint32_t)((uint32_t)(v17) ^ (uint32_t)(v14)) & UINT32_C(0x3fffff));
    uint32_t v19 = ((uint32_t)((uint32_t)(v18) ^ (uint32_t)(v13)) & UINT32_C(0x3fffff));
    uint32_t v20 = ((uint32_t)((uint32_t)(v19) ^ (uint32_t)(v12)) & UINT32_C(0x3fffff));
    uint32_t v21 = ((uint32_t)((uint64_t)a >> 54) & UINT32_C(0x3ff));
    uint32_t v22 = ((uint32_t)((uint64_t)a >> 41) & UINT32_C(0x3ff));
    uint32_t v23 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0x3ff));
    uint32_t v24 = ((uint32_t)((uint64_t)b >> 22) & UINT32_C(0x3ff));
    uint32_t v25 = ((uint32_t)((uint32_t)(v24) ^ (uint32_t)(v23)) & UINT32_C(0x3ff));
    uint32_t v26 = ((uint32_t)((uint32_t)(v25) ^ (uint32_t)(v22)) & UINT32_C(0x3ff));
    uint32_t v27 = ((uint32_t)((uint32_t)(v26) ^ (uint32_t)(v21)) & UINT32_C(0x3ff));
    uint32_t v28 = ((uint32_t)((uint64_t)a >> 51) & UINT32_C(0x1fff));
    uint32_t v29 = ((uint32_t)((uint64_t)a >> 42) & UINT32_C(0x1fff));
    uint32_t v30 = ((uint32_t)((uint64_t)b >> 32) & UINT32_C(0x1fff));
    uint32_t v31 = ((uint32_t)((uint32_t)(v30) ^ (uint32_t)(v29)) & UINT32_C(0x1fff));
    uint32_t v32 = ((uint32_t)((uint32_t)(v31) ^ (uint32_t)(v28)) & UINT32_C(0x1fff));
    uint32_t v33 = ((uint32_t)((uint64_t)a >> 55) & UINT32_C(0x3f));
    uint32_t v34 = ((uint32_t)((uint64_t)b >> 45) & UINT32_C(0x3f));
    uint32_t v35 = ((uint32_t)((uint32_t)(v34) ^ (uint32_t)(v33)) & UINT32_C(0x3f));
    uint32_t v36 = v4;
    uint32_t v37 = v11;
    uint32_t v38 = v20;
    uint32_t v39 = v27;
    uint32_t v40 = v32;
    uint32_t v41 = v35;
    uint32_t v42 = ((uint32_t)(((uint32_t)(v41) << 13) | (uint32_t)(v40)) & UINT32_C(0x7ffff));
    uint32_t v43 = ((uint32_t)(((uint32_t)(v42) << 10) | (uint32_t)(v39)) & UINT32_C(0x1fffffff));
    uint64_t v44 = ((uint64_t)(((uint64_t)(v43) << 22) | (uint64_t)(v38)) & UINT64_C(0x7ffffffffffff));
    uint64_t v45 = ((uint64_t)(((uint64_t)(v44) << 10) | (uint64_t)(v37)) & UINT64_C(0x1fffffffffffffff));
    uint64_t v46 = (uint64_t)(((uint64_t)(v45) << 3) | (uint64_t)(v36));
    return (uint64_t)(v46);
}
