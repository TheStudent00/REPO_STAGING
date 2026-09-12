/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of addw_gpr_gpr_gpr_32__reg_a0__c__all_constructed.  The term's text, LITERAL:
   Concat(Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract */
#include <stdint.h>

uint64_t
emu_addw_gpr_gpr_gpr_32__reg_a0__c__all_constructed(uint32_t a, uint32_t b)
{
    uint32_t v0 = (uint32_t)b;
    uint32_t v1 = (uint32_t)a;
    uint32_t v2 = (uint32_t)((uint32_t)(v1) & (uint32_t)(v0));
    uint32_t v3 = (uint32_t)((uint32_t)(v2) << (unsigned)(uint32_t)(UINT32_C(0x1)));
    uint32_t v4 = (uint32_t)((uint32_t)(v1) ^ (uint32_t)(v0));
    uint32_t v5 = (uint32_t)((uint32_t)(v4) & (uint32_t)(v3));
    uint32_t v6 = (uint32_t)((uint32_t)(v2) | (uint32_t)(v5));
    uint32_t v7 = (uint32_t)((uint32_t)(v6) << (unsigned)(uint32_t)(UINT32_C(0x2)));
    uint32_t v8 = (uint32_t)((uint32_t)(v4) << (unsigned)(uint32_t)(UINT32_C(0x1)));
    uint32_t v9 = (uint32_t)((uint32_t)(v4) & (uint32_t)(v8));
    uint32_t v10 = (uint32_t)((uint32_t)(v9) & (uint32_t)(v7));
    uint32_t v11 = (uint32_t)((uint32_t)(v6) | (uint32_t)(v10));
    uint32_t v12 = (uint32_t)((uint32_t)(v11) << (unsigned)(uint32_t)(UINT32_C(0x4)));
    uint32_t v13 = (uint32_t)((uint32_t)(v9) << (unsigned)(uint32_t)(UINT32_C(0x2)));
    uint32_t v14 = (uint32_t)((uint32_t)(v9) & (uint32_t)(v13));
    uint32_t v15 = (uint32_t)((uint32_t)(v14) & (uint32_t)(v12));
    uint32_t v16 = (uint32_t)((uint32_t)(v11) | (uint32_t)(v15));
    uint32_t v17 = (uint32_t)((uint32_t)(v16) << (unsigned)(uint32_t)(UINT32_C(0x8)));
    uint32_t v18 = (uint32_t)((uint32_t)(v14) << (unsigned)(uint32_t)(UINT32_C(0x4)));
    uint32_t v19 = (uint32_t)((uint32_t)(v14) & (uint32_t)(v18));
    uint32_t v20 = (uint32_t)((uint32_t)(v19) & (uint32_t)(v17));
    uint32_t v21 = (uint32_t)((uint32_t)(v16) | (uint32_t)(v20));
    uint32_t v22 = (uint32_t)((uint32_t)(v21) << (unsigned)(uint32_t)(UINT32_C(0x10)));
    uint32_t v23 = (uint32_t)((uint32_t)(v19) << (unsigned)(uint32_t)(UINT32_C(0x8)));
    uint32_t v24 = (uint32_t)((uint32_t)(v19) & (uint32_t)(v23));
    uint32_t v25 = (uint32_t)((uint32_t)(v24) & (uint32_t)(v22));
    uint32_t v26 = (uint32_t)((uint32_t)(v21) | (uint32_t)(v25));
    uint32_t v27 = (uint32_t)((uint32_t)(v26) << (unsigned)(uint32_t)(UINT32_C(0x1)));
    uint32_t v28 = (uint32_t)((uint32_t)(v4) ^ (uint32_t)(v27));
    uint32_t v29 = ((uint32_t)((uint32_t)(v28) >> 31) & UINT32_C(0x1));
    uint32_t v30 = v28;
    uint32_t v31 = v29;
    uint32_t v32 = ((uint32_t)(((uint32_t)(v31) << 1) | (uint32_t)(v31)) & UINT32_C(0x3));
    uint32_t v33 = ((uint32_t)(((uint32_t)(v32) << 1) | (uint32_t)(v31)) & UINT32_C(0x7));
    uint32_t v34 = ((uint32_t)(((uint32_t)(v33) << 1) | (uint32_t)(v31)) & UINT32_C(0xf));
    uint32_t v35 = ((uint32_t)(((uint32_t)(v34) << 1) | (uint32_t)(v31)) & UINT32_C(0x1f));
    uint32_t v36 = ((uint32_t)(((uint32_t)(v35) << 1) | (uint32_t)(v31)) & UINT32_C(0x3f));
    uint32_t v37 = ((uint32_t)(((uint32_t)(v36) << 1) | (uint32_t)(v31)) & UINT32_C(0x7f));
    uint32_t v38 = ((uint32_t)(((uint32_t)(v37) << 1) | (uint32_t)(v31)) & UINT32_C(0xff));
    uint32_t v39 = ((uint32_t)(((uint32_t)(v38) << 1) | (uint32_t)(v31)) & UINT32_C(0x1ff));
    uint32_t v40 = ((uint32_t)(((uint32_t)(v39) << 1) | (uint32_t)(v31)) & UINT32_C(0x3ff));
    uint32_t v41 = ((uint32_t)(((uint32_t)(v40) << 1) | (uint32_t)(v31)) & UINT32_C(0x7ff));
    uint32_t v42 = ((uint32_t)(((uint32_t)(v41) << 1) | (uint32_t)(v31)) & UINT32_C(0xfff));
    uint32_t v43 = ((uint32_t)(((uint32_t)(v42) << 1) | (uint32_t)(v31)) & UINT32_C(0x1fff));
    uint32_t v44 = ((uint32_t)(((uint32_t)(v43) << 1) | (uint32_t)(v31)) & UINT32_C(0x3fff));
    uint32_t v45 = ((uint32_t)(((uint32_t)(v44) << 1) | (uint32_t)(v31)) & UINT32_C(0x7fff));
    uint32_t v46 = ((uint32_t)(((uint32_t)(v45) << 1) | (uint32_t)(v31)) & UINT32_C(0xffff));
    uint32_t v47 = ((uint32_t)(((uint32_t)(v46) << 1) | (uint32_t)(v31)) & UINT32_C(0x1ffff));
    uint32_t v48 = ((uint32_t)(((uint32_t)(v47) << 1) | (uint32_t)(v31)) & UINT32_C(0x3ffff));
    uint32_t v49 = ((uint32_t)(((uint32_t)(v48) << 1) | (uint32_t)(v31)) & UINT32_C(0x7ffff));
    uint32_t v50 = ((uint32_t)(((uint32_t)(v49) << 1) | (uint32_t)(v31)) & UINT32_C(0xfffff));
    uint32_t v51 = ((uint32_t)(((uint32_t)(v50) << 1) | (uint32_t)(v31)) & UINT32_C(0x1fffff));
    uint32_t v52 = ((uint32_t)(((uint32_t)(v51) << 1) | (uint32_t)(v31)) & UINT32_C(0x3fffff));
    uint32_t v53 = ((uint32_t)(((uint32_t)(v52) << 1) | (uint32_t)(v31)) & UINT32_C(0x7fffff));
    uint32_t v54 = ((uint32_t)(((uint32_t)(v53) << 1) | (uint32_t)(v31)) & UINT32_C(0xffffff));
    uint32_t v55 = ((uint32_t)(((uint32_t)(v54) << 1) | (uint32_t)(v31)) & UINT32_C(0x1ffffff));
    uint32_t v56 = ((uint32_t)(((uint32_t)(v55) << 1) | (uint32_t)(v31)) & UINT32_C(0x3ffffff));
    uint32_t v57 = ((uint32_t)(((uint32_t)(v56) << 1) | (uint32_t)(v31)) & UINT32_C(0x7ffffff));
    uint32_t v58 = ((uint32_t)(((uint32_t)(v57) << 1) | (uint32_t)(v31)) & UINT32_C(0xfffffff));
    uint32_t v59 = ((uint32_t)(((uint32_t)(v58) << 1) | (uint32_t)(v31)) & UINT32_C(0x1fffffff));
    uint32_t v60 = ((uint32_t)(((uint32_t)(v59) << 1) | (uint32_t)(v31)) & UINT32_C(0x3fffffff));
    uint32_t v61 = ((uint32_t)(((uint32_t)(v60) << 1) | (uint32_t)(v31)) & UINT32_C(0x7fffffff));
    uint32_t v62 = (uint32_t)(((uint32_t)(v61) << 1) | (uint32_t)(v31));
    uint64_t v63 = (uint64_t)(((uint64_t)(v62) << 32) | (uint64_t)(v30));
    return (uint64_t)(v63);
}
