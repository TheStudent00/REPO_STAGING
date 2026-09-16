/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of ITYPE__op_ANDI__rd__cpp__all_constructed.  The term's text, LITERAL:
    */
#include <cstdint>

extern "C"
uint64_t
emu_ITYPE__op_ANDI__rd__cpp__all_constructed(uint64_t a, uint16_t b)
{
    uint32_t v0 = ((uint32_t)((uint32_t)b >> 0) & UINT32_C(0xfff));
    uint32_t v1 = ((uint32_t)(~(uint32_t)(v0)) & UINT32_C(0xfff));
    uint32_t v2 = ((uint32_t)((uint32_t)b >> 11) & UINT32_C(0x1));
    uint32_t v3 = ((uint32_t)(~(uint32_t)(v2)) & UINT32_C(0x1));
    uint32_t v4 = v1;
    uint32_t v5 = v3;
    uint32_t v6 = ((uint32_t)(((uint32_t)(v5) << 1) | (uint32_t)(v5)) & UINT32_C(0x3));
    uint32_t v7 = ((uint32_t)(((uint32_t)(v6) << 1) | (uint32_t)(v5)) & UINT32_C(0x7));
    uint32_t v8 = ((uint32_t)(((uint32_t)(v7) << 1) | (uint32_t)(v5)) & UINT32_C(0xf));
    uint32_t v9 = ((uint32_t)(((uint32_t)(v8) << 1) | (uint32_t)(v5)) & UINT32_C(0x1f));
    uint32_t v10 = ((uint32_t)(((uint32_t)(v9) << 1) | (uint32_t)(v5)) & UINT32_C(0x3f));
    uint32_t v11 = ((uint32_t)(((uint32_t)(v10) << 1) | (uint32_t)(v5)) & UINT32_C(0x7f));
    uint32_t v12 = ((uint32_t)(((uint32_t)(v11) << 1) | (uint32_t)(v5)) & UINT32_C(0xff));
    uint32_t v13 = ((uint32_t)(((uint32_t)(v12) << 1) | (uint32_t)(v5)) & UINT32_C(0x1ff));
    uint32_t v14 = ((uint32_t)(((uint32_t)(v13) << 1) | (uint32_t)(v5)) & UINT32_C(0x3ff));
    uint32_t v15 = ((uint32_t)(((uint32_t)(v14) << 1) | (uint32_t)(v5)) & UINT32_C(0x7ff));
    uint32_t v16 = ((uint32_t)(((uint32_t)(v15) << 1) | (uint32_t)(v5)) & UINT32_C(0xfff));
    uint32_t v17 = ((uint32_t)(((uint32_t)(v16) << 1) | (uint32_t)(v5)) & UINT32_C(0x1fff));
    uint32_t v18 = ((uint32_t)(((uint32_t)(v17) << 1) | (uint32_t)(v5)) & UINT32_C(0x3fff));
    uint32_t v19 = ((uint32_t)(((uint32_t)(v18) << 1) | (uint32_t)(v5)) & UINT32_C(0x7fff));
    uint32_t v20 = ((uint32_t)(((uint32_t)(v19) << 1) | (uint32_t)(v5)) & UINT32_C(0xffff));
    uint32_t v21 = ((uint32_t)(((uint32_t)(v20) << 1) | (uint32_t)(v5)) & UINT32_C(0x1ffff));
    uint32_t v22 = ((uint32_t)(((uint32_t)(v21) << 1) | (uint32_t)(v5)) & UINT32_C(0x3ffff));
    uint32_t v23 = ((uint32_t)(((uint32_t)(v22) << 1) | (uint32_t)(v5)) & UINT32_C(0x7ffff));
    uint32_t v24 = ((uint32_t)(((uint32_t)(v23) << 1) | (uint32_t)(v5)) & UINT32_C(0xfffff));
    uint32_t v25 = ((uint32_t)(((uint32_t)(v24) << 1) | (uint32_t)(v5)) & UINT32_C(0x1fffff));
    uint32_t v26 = ((uint32_t)(((uint32_t)(v25) << 1) | (uint32_t)(v5)) & UINT32_C(0x3fffff));
    uint32_t v27 = ((uint32_t)(((uint32_t)(v26) << 1) | (uint32_t)(v5)) & UINT32_C(0x7fffff));
    uint32_t v28 = ((uint32_t)(((uint32_t)(v27) << 1) | (uint32_t)(v5)) & UINT32_C(0xffffff));
    uint32_t v29 = ((uint32_t)(((uint32_t)(v28) << 1) | (uint32_t)(v5)) & UINT32_C(0x1ffffff));
    uint32_t v30 = ((uint32_t)(((uint32_t)(v29) << 1) | (uint32_t)(v5)) & UINT32_C(0x3ffffff));
    uint32_t v31 = ((uint32_t)(((uint32_t)(v30) << 1) | (uint32_t)(v5)) & UINT32_C(0x7ffffff));
    uint32_t v32 = ((uint32_t)(((uint32_t)(v31) << 1) | (uint32_t)(v5)) & UINT32_C(0xfffffff));
    uint32_t v33 = ((uint32_t)(((uint32_t)(v32) << 1) | (uint32_t)(v5)) & UINT32_C(0x1fffffff));
    uint32_t v34 = ((uint32_t)(((uint32_t)(v33) << 1) | (uint32_t)(v5)) & UINT32_C(0x3fffffff));
    uint32_t v35 = ((uint32_t)(((uint32_t)(v34) << 1) | (uint32_t)(v5)) & UINT32_C(0x7fffffff));
    uint32_t v36 = (uint32_t)(((uint32_t)(v35) << 1) | (uint32_t)(v5));
    uint64_t v37 = ((uint64_t)(((uint64_t)(v36) << 1) | (uint64_t)(v5)) & UINT64_C(0x1ffffffff));
    uint64_t v38 = ((uint64_t)(((uint64_t)(v37) << 1) | (uint64_t)(v5)) & UINT64_C(0x3ffffffff));
    uint64_t v39 = ((uint64_t)(((uint64_t)(v38) << 1) | (uint64_t)(v5)) & UINT64_C(0x7ffffffff));
    uint64_t v40 = ((uint64_t)(((uint64_t)(v39) << 1) | (uint64_t)(v5)) & UINT64_C(0xfffffffff));
    uint64_t v41 = ((uint64_t)(((uint64_t)(v40) << 1) | (uint64_t)(v5)) & UINT64_C(0x1fffffffff));
    uint64_t v42 = ((uint64_t)(((uint64_t)(v41) << 1) | (uint64_t)(v5)) & UINT64_C(0x3fffffffff));
    uint64_t v43 = ((uint64_t)(((uint64_t)(v42) << 1) | (uint64_t)(v5)) & UINT64_C(0x7fffffffff));
    uint64_t v44 = ((uint64_t)(((uint64_t)(v43) << 1) | (uint64_t)(v5)) & UINT64_C(0xffffffffff));
    uint64_t v45 = ((uint64_t)(((uint64_t)(v44) << 1) | (uint64_t)(v5)) & UINT64_C(0x1ffffffffff));
    uint64_t v46 = ((uint64_t)(((uint64_t)(v45) << 1) | (uint64_t)(v5)) & UINT64_C(0x3ffffffffff));
    uint64_t v47 = ((uint64_t)(((uint64_t)(v46) << 1) | (uint64_t)(v5)) & UINT64_C(0x7ffffffffff));
    uint64_t v48 = ((uint64_t)(((uint64_t)(v47) << 1) | (uint64_t)(v5)) & UINT64_C(0xfffffffffff));
    uint64_t v49 = ((uint64_t)(((uint64_t)(v48) << 1) | (uint64_t)(v5)) & UINT64_C(0x1fffffffffff));
    uint64_t v50 = ((uint64_t)(((uint64_t)(v49) << 1) | (uint64_t)(v5)) & UINT64_C(0x3fffffffffff));
    uint64_t v51 = ((uint64_t)(((uint64_t)(v50) << 1) | (uint64_t)(v5)) & UINT64_C(0x7fffffffffff));
    uint64_t v52 = ((uint64_t)(((uint64_t)(v51) << 1) | (uint64_t)(v5)) & UINT64_C(0xffffffffffff));
    uint64_t v53 = ((uint64_t)(((uint64_t)(v52) << 1) | (uint64_t)(v5)) & UINT64_C(0x1ffffffffffff));
    uint64_t v54 = ((uint64_t)(((uint64_t)(v53) << 1) | (uint64_t)(v5)) & UINT64_C(0x3ffffffffffff));
    uint64_t v55 = ((uint64_t)(((uint64_t)(v54) << 1) | (uint64_t)(v5)) & UINT64_C(0x7ffffffffffff));
    uint64_t v56 = ((uint64_t)(((uint64_t)(v55) << 12) | (uint64_t)(v4)) & UINT64_C(0x7fffffffffffffff));
    uint64_t v57 = ((uint64_t)((uint64_t)a >> 0) & UINT64_C(0x7fffffffffffffff));
    uint64_t v58 = ((uint64_t)(~(uint64_t)(v57)) & UINT64_C(0x7fffffffffffffff));
    uint64_t v59 = ((uint64_t)((uint64_t)(v58) | (uint64_t)(v56)) & UINT64_C(0x7fffffffffffffff));
    uint64_t v60 = ((uint64_t)(~(uint64_t)(v59)) & UINT64_C(0x7fffffffffffffff));
    uint32_t v61 = ((uint32_t)((uint64_t)a >> 63) & UINT32_C(0x1));
    uint32_t v62 = ((uint32_t)(~(uint32_t)(v61)) & UINT32_C(0x1));
    uint32_t v63 = ((uint32_t)((uint32_t)(v3) | (uint32_t)(v62)) & UINT32_C(0x1));
    uint32_t v64 = ((uint32_t)(~(uint32_t)(v63)) & UINT32_C(0x1));
    uint64_t v65 = v60;
    uint32_t v66 = v64;
    uint64_t v67 = (uint64_t)(((uint64_t)(v66) << 63) | (uint64_t)(v65));
    return (uint64_t)(v67);
}
