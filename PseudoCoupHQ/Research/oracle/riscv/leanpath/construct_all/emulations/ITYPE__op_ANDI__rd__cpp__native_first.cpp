/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of ITYPE__op_ANDI__rd__cpp__native_first.  The term's text, LITERAL:
    */
#include <cstdint>

extern "C"
uint64_t
emu_ITYPE__op_ANDI__rd__cpp__native_first(uint64_t a, uint16_t b)
{
    uint32_t v0 = ((uint32_t)((uint32_t)b >> 0) & UINT32_C(0xfff));
    uint32_t v1 = ((uint32_t)(~(uint32_t)(v0)) & UINT32_C(0xfff));
    uint32_t v2 = ((uint32_t)((uint32_t)b >> 11) & UINT32_C(0x1));
    uint32_t v3 = ((uint32_t)(~(uint32_t)(v2)) & UINT32_C(0x1));
    uint64_t v4 = ((uint64_t)(((uint64_t)(v3) << 62) | ((uint64_t)(v3) << 61) | ((uint64_t)(v3) << 60) | ((uint64_t)(v3) << 59) | ((uint64_t)(v3) << 58) | ((uint64_t)(v3) << 57) | ((uint64_t)(v3) << 56) | ((uint64_t)(v3) << 55) | ((uint64_t)(v3) << 54) | ((uint64_t)(v3) << 53) | ((uint64_t)(v3) << 52) | ((uint64_t)(v3) << 51) | ((uint64_t)(v3) << 50) | ((uint64_t)(v3) << 49) | ((uint64_t)(v3) << 48) | ((uint64_t)(v3) << 47) | ((uint64_t)(v3) << 46) | ((uint64_t)(v3) << 45) | ((uint64_t)(v3) << 44) | ((uint64_t)(v3) << 43) | ((uint64_t)(v3) << 42) | ((uint64_t)(v3) << 41) | ((uint64_t)(v3) << 40) | ((uint64_t)(v3) << 39) | ((uint64_t)(v3) << 38) | ((uint64_t)(v3) << 37) | ((uint64_t)(v3) << 36) | ((uint64_t)(v3) << 35) | ((uint64_t)(v3) << 34) | ((uint64_t)(v3) << 33) | ((uint64_t)(v3) << 32) | ((uint64_t)(v3) << 31) | ((uint64_t)(v3) << 30) | ((uint64_t)(v3) << 29) | ((uint64_t)(v3) << 28) | ((uint64_t)(v3) << 27) | ((uint64_t)(v3) << 26) | ((uint64_t)(v3) << 25) | ((uint64_t)(v3) << 24) | ((uint64_t)(v3) << 23) | ((uint64_t)(v3) << 22) | ((uint64_t)(v3) << 21) | ((uint64_t)(v3) << 20) | ((uint64_t)(v3) << 19) | ((uint64_t)(v3) << 18) | ((uint64_t)(v3) << 17) | ((uint64_t)(v3) << 16) | ((uint64_t)(v3) << 15) | ((uint64_t)(v3) << 14) | ((uint64_t)(v3) << 13) | ((uint64_t)(v3) << 12) | (uint64_t)(v1)) & UINT64_C(0x7fffffffffffffff));
    uint64_t v5 = ((uint64_t)((uint64_t)a >> 0) & UINT64_C(0x7fffffffffffffff));
    uint64_t v6 = ((uint64_t)(~(uint64_t)(v5)) & UINT64_C(0x7fffffffffffffff));
    uint64_t v7 = ((uint64_t)((uint64_t)(v6) | (uint64_t)(v4)) & UINT64_C(0x7fffffffffffffff));
    uint64_t v8 = ((uint64_t)(~(uint64_t)(v7)) & UINT64_C(0x7fffffffffffffff));
    uint32_t v9 = ((uint32_t)((uint64_t)a >> 63) & UINT32_C(0x1));
    uint32_t v10 = ((uint32_t)(~(uint32_t)(v9)) & UINT32_C(0x1));
    uint32_t v11 = ((uint32_t)((uint32_t)(v3) | (uint32_t)(v10)) & UINT32_C(0x1));
    uint32_t v12 = ((uint32_t)(~(uint32_t)(v11)) & UINT32_C(0x1));
    uint64_t v13 = (uint64_t)(((uint64_t)(v12) << 63) | (uint64_t)(v8));
    return (uint64_t)(v13);
}
