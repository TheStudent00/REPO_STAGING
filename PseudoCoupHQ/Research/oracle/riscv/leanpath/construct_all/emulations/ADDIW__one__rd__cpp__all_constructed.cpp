/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of ADDIW__one__rd__cpp__all_constructed.  The term's text, LITERAL:
    */
#include <cstdint>

extern "C"
uint64_t
emu_ADDIW__one__rd__cpp__all_constructed(uint32_t a, uint16_t b)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = ((uint32_t)((uint32_t)b >> 0) & UINT32_C(0xfff));
    uint32_t v2 = ((uint32_t)((uint32_t)b >> 11) & UINT32_C(0x1));
    uint32_t v3 = v1;
    uint32_t v4 = v2;
    uint32_t v5 = ((uint32_t)(((uint32_t)(v4) << 1) | (uint32_t)(v4)) & UINT32_C(0x3));
    uint32_t v6 = ((uint32_t)(((uint32_t)(v5) << 1) | (uint32_t)(v4)) & UINT32_C(0x7));
    uint32_t v7 = ((uint32_t)(((uint32_t)(v6) << 1) | (uint32_t)(v4)) & UINT32_C(0xf));
    uint32_t v8 = ((uint32_t)(((uint32_t)(v7) << 1) | (uint32_t)(v4)) & UINT32_C(0x1f));
    uint32_t v9 = ((uint32_t)(((uint32_t)(v8) << 1) | (uint32_t)(v4)) & UINT32_C(0x3f));
    uint32_t v10 = ((uint32_t)(((uint32_t)(v9) << 1) | (uint32_t)(v4)) & UINT32_C(0x7f));
    uint32_t v11 = ((uint32_t)(((uint32_t)(v10) << 1) | (uint32_t)(v4)) & UINT32_C(0xff));
    uint32_t v12 = ((uint32_t)(((uint32_t)(v11) << 1) | (uint32_t)(v4)) & UINT32_C(0x1ff));
    uint32_t v13 = ((uint32_t)(((uint32_t)(v12) << 1) | (uint32_t)(v4)) & UINT32_C(0x3ff));
    uint32_t v14 = ((uint32_t)(((uint32_t)(v13) << 1) | (uint32_t)(v4)) & UINT32_C(0x7ff));
    uint32_t v15 = ((uint32_t)(((uint32_t)(v14) << 1) | (uint32_t)(v4)) & UINT32_C(0xfff));
    uint32_t v16 = ((uint32_t)(((uint32_t)(v15) << 1) | (uint32_t)(v4)) & UINT32_C(0x1fff));
    uint32_t v17 = ((uint32_t)(((uint32_t)(v16) << 1) | (uint32_t)(v4)) & UINT32_C(0x3fff));
    uint32_t v18 = ((uint32_t)(((uint32_t)(v17) << 1) | (uint32_t)(v4)) & UINT32_C(0x7fff));
    uint32_t v19 = ((uint32_t)(((uint32_t)(v18) << 1) | (uint32_t)(v4)) & UINT32_C(0xffff));
    uint32_t v20 = ((uint32_t)(((uint32_t)(v19) << 1) | (uint32_t)(v4)) & UINT32_C(0x1ffff));
    uint32_t v21 = ((uint32_t)(((uint32_t)(v20) << 1) | (uint32_t)(v4)) & UINT32_C(0x3ffff));
    uint32_t v22 = ((uint32_t)(((uint32_t)(v21) << 1) | (uint32_t)(v4)) & UINT32_C(0x7ffff));
    uint32_t v23 = ((uint32_t)(((uint32_t)(v22) << 1) | (uint32_t)(v4)) & UINT32_C(0xfffff));
    uint32_t v24 = (uint32_t)(((uint32_t)(v23) << 12) | (uint32_t)(v3));
    uint32_t v25 = (uint32_t)((uint32_t)(v24) & (uint32_t)(v0));
    uint32_t v26 = (uint32_t)((uint32_t)(v25) << (unsigned)(uint32_t)(UINT32_C(0x1)));
    uint32_t v27 = (uint32_t)((uint32_t)(v24) ^ (uint32_t)(v0));
    uint32_t v28 = (uint32_t)((uint32_t)(v27) & (uint32_t)(v26));
    uint32_t v29 = (uint32_t)((uint32_t)(v25) | (uint32_t)(v28));
    uint32_t v30 = (uint32_t)((uint32_t)(v29) << (unsigned)(uint32_t)(UINT32_C(0x2)));
    uint32_t v31 = (uint32_t)((uint32_t)(v27) << (unsigned)(uint32_t)(UINT32_C(0x1)));
    uint32_t v32 = (uint32_t)((uint32_t)(v27) & (uint32_t)(v31));
    uint32_t v33 = (uint32_t)((uint32_t)(v32) & (uint32_t)(v30));
    uint32_t v34 = (uint32_t)((uint32_t)(v29) | (uint32_t)(v33));
    uint32_t v35 = (uint32_t)((uint32_t)(v34) << (unsigned)(uint32_t)(UINT32_C(0x4)));
    uint32_t v36 = (uint32_t)((uint32_t)(v32) << (unsigned)(uint32_t)(UINT32_C(0x2)));
    uint32_t v37 = (uint32_t)((uint32_t)(v32) & (uint32_t)(v36));
    uint32_t v38 = (uint32_t)((uint32_t)(v37) & (uint32_t)(v35));
    uint32_t v39 = (uint32_t)((uint32_t)(v34) | (uint32_t)(v38));
    uint32_t v40 = (uint32_t)((uint32_t)(v39) << (unsigned)(uint32_t)(UINT32_C(0x8)));
    uint32_t v41 = (uint32_t)((uint32_t)(v37) << (unsigned)(uint32_t)(UINT32_C(0x4)));
    uint32_t v42 = (uint32_t)((uint32_t)(v37) & (uint32_t)(v41));
    uint32_t v43 = (uint32_t)((uint32_t)(v42) & (uint32_t)(v40));
    uint32_t v44 = (uint32_t)((uint32_t)(v39) | (uint32_t)(v43));
    uint32_t v45 = (uint32_t)((uint32_t)(v44) << (unsigned)(uint32_t)(UINT32_C(0x10)));
    uint32_t v46 = (uint32_t)((uint32_t)(v42) << (unsigned)(uint32_t)(UINT32_C(0x8)));
    uint32_t v47 = (uint32_t)((uint32_t)(v42) & (uint32_t)(v46));
    uint32_t v48 = (uint32_t)((uint32_t)(v47) & (uint32_t)(v45));
    uint32_t v49 = (uint32_t)((uint32_t)(v44) | (uint32_t)(v48));
    uint32_t v50 = (uint32_t)((uint32_t)(v49) << (unsigned)(uint32_t)(UINT32_C(0x1)));
    uint32_t v51 = (uint32_t)((uint32_t)(v27) ^ (uint32_t)(v50));
    uint32_t v52 = ((uint32_t)((uint32_t)(v51) >> 31) & UINT32_C(0x1));
    uint32_t v53 = v51;
    uint32_t v54 = v52;
    uint32_t v55 = ((uint32_t)(((uint32_t)(v54) << 1) | (uint32_t)(v54)) & UINT32_C(0x3));
    uint32_t v56 = ((uint32_t)(((uint32_t)(v55) << 1) | (uint32_t)(v54)) & UINT32_C(0x7));
    uint32_t v57 = ((uint32_t)(((uint32_t)(v56) << 1) | (uint32_t)(v54)) & UINT32_C(0xf));
    uint32_t v58 = ((uint32_t)(((uint32_t)(v57) << 1) | (uint32_t)(v54)) & UINT32_C(0x1f));
    uint32_t v59 = ((uint32_t)(((uint32_t)(v58) << 1) | (uint32_t)(v54)) & UINT32_C(0x3f));
    uint32_t v60 = ((uint32_t)(((uint32_t)(v59) << 1) | (uint32_t)(v54)) & UINT32_C(0x7f));
    uint32_t v61 = ((uint32_t)(((uint32_t)(v60) << 1) | (uint32_t)(v54)) & UINT32_C(0xff));
    uint32_t v62 = ((uint32_t)(((uint32_t)(v61) << 1) | (uint32_t)(v54)) & UINT32_C(0x1ff));
    uint32_t v63 = ((uint32_t)(((uint32_t)(v62) << 1) | (uint32_t)(v54)) & UINT32_C(0x3ff));
    uint32_t v64 = ((uint32_t)(((uint32_t)(v63) << 1) | (uint32_t)(v54)) & UINT32_C(0x7ff));
    uint32_t v65 = ((uint32_t)(((uint32_t)(v64) << 1) | (uint32_t)(v54)) & UINT32_C(0xfff));
    uint32_t v66 = ((uint32_t)(((uint32_t)(v65) << 1) | (uint32_t)(v54)) & UINT32_C(0x1fff));
    uint32_t v67 = ((uint32_t)(((uint32_t)(v66) << 1) | (uint32_t)(v54)) & UINT32_C(0x3fff));
    uint32_t v68 = ((uint32_t)(((uint32_t)(v67) << 1) | (uint32_t)(v54)) & UINT32_C(0x7fff));
    uint32_t v69 = ((uint32_t)(((uint32_t)(v68) << 1) | (uint32_t)(v54)) & UINT32_C(0xffff));
    uint32_t v70 = ((uint32_t)(((uint32_t)(v69) << 1) | (uint32_t)(v54)) & UINT32_C(0x1ffff));
    uint32_t v71 = ((uint32_t)(((uint32_t)(v70) << 1) | (uint32_t)(v54)) & UINT32_C(0x3ffff));
    uint32_t v72 = ((uint32_t)(((uint32_t)(v71) << 1) | (uint32_t)(v54)) & UINT32_C(0x7ffff));
    uint32_t v73 = ((uint32_t)(((uint32_t)(v72) << 1) | (uint32_t)(v54)) & UINT32_C(0xfffff));
    uint32_t v74 = ((uint32_t)(((uint32_t)(v73) << 1) | (uint32_t)(v54)) & UINT32_C(0x1fffff));
    uint32_t v75 = ((uint32_t)(((uint32_t)(v74) << 1) | (uint32_t)(v54)) & UINT32_C(0x3fffff));
    uint32_t v76 = ((uint32_t)(((uint32_t)(v75) << 1) | (uint32_t)(v54)) & UINT32_C(0x7fffff));
    uint32_t v77 = ((uint32_t)(((uint32_t)(v76) << 1) | (uint32_t)(v54)) & UINT32_C(0xffffff));
    uint32_t v78 = ((uint32_t)(((uint32_t)(v77) << 1) | (uint32_t)(v54)) & UINT32_C(0x1ffffff));
    uint32_t v79 = ((uint32_t)(((uint32_t)(v78) << 1) | (uint32_t)(v54)) & UINT32_C(0x3ffffff));
    uint32_t v80 = ((uint32_t)(((uint32_t)(v79) << 1) | (uint32_t)(v54)) & UINT32_C(0x7ffffff));
    uint32_t v81 = ((uint32_t)(((uint32_t)(v80) << 1) | (uint32_t)(v54)) & UINT32_C(0xfffffff));
    uint32_t v82 = ((uint32_t)(((uint32_t)(v81) << 1) | (uint32_t)(v54)) & UINT32_C(0x1fffffff));
    uint32_t v83 = ((uint32_t)(((uint32_t)(v82) << 1) | (uint32_t)(v54)) & UINT32_C(0x3fffffff));
    uint32_t v84 = ((uint32_t)(((uint32_t)(v83) << 1) | (uint32_t)(v54)) & UINT32_C(0x7fffffff));
    uint32_t v85 = (uint32_t)(((uint32_t)(v84) << 1) | (uint32_t)(v54));
    uint64_t v86 = (uint64_t)(((uint64_t)(v85) << 32) | (uint64_t)(v53));
    return (uint64_t)(v86);
}
