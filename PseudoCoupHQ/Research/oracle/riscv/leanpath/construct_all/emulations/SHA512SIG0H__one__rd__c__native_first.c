/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of SHA512SIG0H__one__rd__c__native_first.  The term's text, LITERAL:
    */
#include <stdint.h>

uint64_t
emu_SHA512SIG0H__one__rd__c__native_first(uint64_t a, uint64_t b)
{
    uint32_t v0 = ((uint32_t)((uint64_t)a >> 8) & UINT32_C(0xffffff));
    uint32_t v1 = ((uint32_t)((uint64_t)a >> 7) & UINT32_C(0xffffff));
    uint32_t v2 = ((uint32_t)((uint64_t)a >> 1) & UINT32_C(0xffffff));
    uint32_t v3 = ((uint32_t)((uint32_t)(v2) ^ (uint32_t)(v1) ^ (uint32_t)(v0)) & UINT32_C(0xffffff));
    uint32_t v4 = ((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x7f));
    uint32_t v5 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0x7f));
    uint32_t v6 = ((uint32_t)((uint64_t)a >> 31) & UINT32_C(0x7f));
    uint32_t v7 = ((uint32_t)((uint64_t)a >> 25) & UINT32_C(0x7f));
    uint32_t v8 = ((uint32_t)((uint32_t)(v7) ^ (uint32_t)(v6) ^ (uint32_t)(v5) ^ (uint32_t)(v4)) & UINT32_C(0x7f));
    uint32_t v9 = ((uint32_t)((uint64_t)a >> 39) & UINT32_C(0x1ffffff));
    uint32_t v10 = ((uint32_t)((uint64_t)a >> 38) & UINT32_C(0x1ffffff));
    uint32_t v11 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0x1ffffff));
    uint32_t v12 = ((uint32_t)((uint64_t)b >> 7) & UINT32_C(0x1ffffff));
    uint32_t v13 = ((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x1ffffff));
    uint32_t v14 = ((uint32_t)((uint32_t)(v13) ^ (uint32_t)(v12) ^ (uint32_t)(v11) ^ (uint32_t)(v10) ^ (uint32_t)(v9)) & UINT32_C(0x1ffffff));
    uint32_t v15 = ((uint32_t)((uint64_t)a >> 63) & UINT32_C(0x1));
    uint32_t v16 = ((uint32_t)((uint64_t)a >> 57) & UINT32_C(0x1));
    uint32_t v17 = ((uint32_t)((uint64_t)b >> 32) & UINT32_C(0x1));
    uint32_t v18 = ((uint32_t)((uint64_t)b >> 25) & UINT32_C(0x1));
    uint32_t v19 = ((uint32_t)((uint32_t)(v18) ^ (uint32_t)(v17) ^ (uint32_t)(v16) ^ (uint32_t)(v15)) & UINT32_C(0x1));
    uint32_t v20 = ((uint32_t)((uint64_t)a >> 58) & UINT32_C(0x3f));
    uint32_t v21 = ((uint32_t)((uint64_t)b >> 33) & UINT32_C(0x3f));
    uint32_t v22 = ((uint32_t)((uint64_t)b >> 26) & UINT32_C(0x3f));
    uint32_t v23 = ((uint32_t)((uint32_t)(v22) ^ (uint32_t)(v21) ^ (uint32_t)(v20)) & UINT32_C(0x3f));
    uint32_t v24 = ((uint32_t)((uint64_t)b >> 39) & UINT32_C(0x1));
    uint32_t v25 = ((uint32_t)((uint32_t)(v17) ^ (uint32_t)(v24)) & UINT32_C(0x1));
    uint64_t v26 = (uint64_t)(((uint64_t)(v25) << 63) | ((uint64_t)(v23) << 57) | ((uint64_t)(v19) << 56) | ((uint64_t)(v14) << 31) | ((uint64_t)(v8) << 24) | (uint64_t)(v3));
    return (uint64_t)(v26);
}
