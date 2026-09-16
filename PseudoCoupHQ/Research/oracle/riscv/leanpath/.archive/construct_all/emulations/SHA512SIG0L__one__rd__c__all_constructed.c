/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of SHA512SIG0L__one__rd__c__all_constructed.  The term's text, LITERAL:
    */
#include <stdint.h>

uint64_t
emu_SHA512SIG0L__one__rd__c__all_constructed(uint64_t a, uint64_t b)
{
    uint32_t v0 = ((uint32_t)((uint64_t)a >> 8) & UINT32_C(0xffffff));
    uint32_t v1 = ((uint32_t)((uint64_t)a >> 7) & UINT32_C(0xffffff));
    uint32_t v2 = ((uint32_t)((uint64_t)a >> 1) & UINT32_C(0xffffff));
    uint32_t v3 = ((uint32_t)((uint32_t)(v2) ^ (uint32_t)(v1)) & UINT32_C(0xffffff));
    uint32_t v4 = ((uint32_t)((uint32_t)(v3) ^ (uint32_t)(v0)) & UINT32_C(0xffffff));
    uint32_t v5 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0x1));
    uint32_t v6 = ((uint32_t)((uint64_t)a >> 31) & UINT32_C(0x1));
    uint32_t v7 = ((uint32_t)((uint64_t)a >> 25) & UINT32_C(0x1));
    uint32_t v8 = ((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x1));
    uint32_t v9 = ((uint32_t)((uint32_t)(v8) ^ (uint32_t)(v7)) & UINT32_C(0x1));
    uint32_t v10 = ((uint32_t)((uint32_t)(v9) ^ (uint32_t)(v6)) & UINT32_C(0x1));
    uint32_t v11 = ((uint32_t)((uint32_t)(v10) ^ (uint32_t)(v5)) & UINT32_C(0x1));
    uint32_t v12 = ((uint32_t)((uint64_t)b >> 1) & UINT32_C(0x3f));
    uint32_t v13 = ((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x3f));
    uint32_t v14 = ((uint32_t)((uint64_t)a >> 33) & UINT32_C(0x3f));
    uint32_t v15 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0x3f));
    uint32_t v16 = ((uint32_t)((uint64_t)a >> 26) & UINT32_C(0x3f));
    uint32_t v17 = ((uint32_t)((uint32_t)(v16) ^ (uint32_t)(v15)) & UINT32_C(0x3f));
    uint32_t v18 = ((uint32_t)((uint32_t)(v17) ^ (uint32_t)(v14)) & UINT32_C(0x3f));
    uint32_t v19 = ((uint32_t)((uint32_t)(v18) ^ (uint32_t)(v13)) & UINT32_C(0x3f));
    uint32_t v20 = ((uint32_t)((uint32_t)(v19) ^ (uint32_t)(v12)) & UINT32_C(0x3f));
    uint32_t v21 = ((uint32_t)((uint64_t)a >> 39) & UINT32_C(0x1ffffff));
    uint32_t v22 = ((uint32_t)((uint64_t)a >> 38) & UINT32_C(0x1ffffff));
    uint32_t v23 = ((uint32_t)((uint64_t)a >> 32) & UINT32_C(0x1ffffff));
    uint32_t v24 = ((uint32_t)((uint64_t)b >> 7) & UINT32_C(0x1ffffff));
    uint32_t v25 = ((uint32_t)((uint64_t)b >> 6) & UINT32_C(0x1ffffff));
    uint32_t v26 = ((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x1ffffff));
    uint32_t v27 = ((uint32_t)((uint32_t)(v26) ^ (uint32_t)(v25)) & UINT32_C(0x1ffffff));
    uint32_t v28 = ((uint32_t)((uint32_t)(v27) ^ (uint32_t)(v24)) & UINT32_C(0x1ffffff));
    uint32_t v29 = ((uint32_t)((uint32_t)(v28) ^ (uint32_t)(v23)) & UINT32_C(0x1ffffff));
    uint32_t v30 = ((uint32_t)((uint32_t)(v29) ^ (uint32_t)(v22)) & UINT32_C(0x1ffffff));
    uint32_t v31 = ((uint32_t)((uint32_t)(v30) ^ (uint32_t)(v21)) & UINT32_C(0x1ffffff));
    uint32_t v32 = ((uint32_t)((uint64_t)a >> 63) & UINT32_C(0x1));
    uint32_t v33 = ((uint32_t)((uint64_t)a >> 57) & UINT32_C(0x1));
    uint32_t v34 = ((uint32_t)((uint64_t)b >> 32) & UINT32_C(0x1));
    uint32_t v35 = ((uint32_t)((uint64_t)b >> 31) & UINT32_C(0x1));
    uint32_t v36 = ((uint32_t)((uint64_t)b >> 25) & UINT32_C(0x1));
    uint32_t v37 = ((uint32_t)((uint32_t)(v36) ^ (uint32_t)(v35)) & UINT32_C(0x1));
    uint32_t v38 = ((uint32_t)((uint32_t)(v37) ^ (uint32_t)(v34)) & UINT32_C(0x1));
    uint32_t v39 = ((uint32_t)((uint32_t)(v38) ^ (uint32_t)(v33)) & UINT32_C(0x1));
    uint32_t v40 = ((uint32_t)((uint32_t)(v39) ^ (uint32_t)(v32)) & UINT32_C(0x1));
    uint32_t v41 = ((uint32_t)((uint64_t)a >> 58) & UINT32_C(0x3f));
    uint32_t v42 = ((uint32_t)((uint64_t)b >> 33) & UINT32_C(0x3f));
    uint32_t v43 = ((uint32_t)((uint64_t)b >> 32) & UINT32_C(0x3f));
    uint32_t v44 = ((uint32_t)((uint64_t)b >> 26) & UINT32_C(0x3f));
    uint32_t v45 = ((uint32_t)((uint32_t)(v44) ^ (uint32_t)(v43)) & UINT32_C(0x3f));
    uint32_t v46 = ((uint32_t)((uint32_t)(v45) ^ (uint32_t)(v42)) & UINT32_C(0x3f));
    uint32_t v47 = ((uint32_t)((uint32_t)(v46) ^ (uint32_t)(v41)) & UINT32_C(0x3f));
    uint32_t v48 = ((uint32_t)((uint64_t)b >> 39) & UINT32_C(0x1));
    uint32_t v49 = ((uint32_t)((uint64_t)b >> 38) & UINT32_C(0x1));
    uint32_t v50 = ((uint32_t)((uint32_t)(v34) ^ (uint32_t)(v49)) & UINT32_C(0x1));
    uint32_t v51 = ((uint32_t)((uint32_t)(v50) ^ (uint32_t)(v48)) & UINT32_C(0x1));
    uint32_t v52 = v4;
    uint32_t v53 = v11;
    uint32_t v54 = v20;
    uint32_t v55 = v31;
    uint32_t v56 = v40;
    uint32_t v57 = v47;
    uint32_t v58 = v51;
    uint32_t v59 = ((uint32_t)(((uint32_t)(v58) << 6) | (uint32_t)(v57)) & UINT32_C(0x7f));
    uint32_t v60 = ((uint32_t)(((uint32_t)(v59) << 1) | (uint32_t)(v56)) & UINT32_C(0xff));
    uint64_t v61 = ((uint64_t)(((uint64_t)(v60) << 25) | (uint64_t)(v55)) & UINT64_C(0x1ffffffff));
    uint64_t v62 = ((uint64_t)(((uint64_t)(v61) << 6) | (uint64_t)(v54)) & UINT64_C(0x7fffffffff));
    uint64_t v63 = ((uint64_t)(((uint64_t)(v62) << 1) | (uint64_t)(v53)) & UINT64_C(0xffffffffff));
    uint64_t v64 = (uint64_t)(((uint64_t)(v63) << 24) | (uint64_t)(v52));
    return (uint64_t)(v64);
}
