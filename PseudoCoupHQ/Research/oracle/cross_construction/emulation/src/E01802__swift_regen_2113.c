/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01802__swift_regen_2113.  The term's layer-5 text, LITERAL:
   If(0 <= Extract(7, 0, v2), If(Extract(6, 6, v2) == 0, Extract(63, 0, LShR(Concat(v0, v1), Concat(0, Extract(5, 0, v2)))), LShR(v0, Concat(0, Extract(5, 0, v2)))), 0) */
#include <stdint.h>

uint64_t
emu_E01802__swift_regen_2113(uint64_t a, uint64_t b, uint8_t c)
{
    return (uint64_t)((((((int32_t)((uint32_t)(UINT32_C(0x0)) << 24) >> 24) <= ((int32_t)((uint32_t)((uint32_t)c) << 24) >> 24))) ? (uint64_t)(((((uint32_t)(((uint32_t)((uint32_t)c >> 6) & UINT32_C(0x1))) == (uint32_t)(UINT32_C(0x0)))) ? (uint64_t)((uint64_t)((unsigned __int128)((unsigned __int128)((unsigned __int128)((unsigned __int128)(((unsigned __int128)((uint64_t)b) << 64) | (unsigned __int128)((uint64_t)a))) >> (unsigned)(unsigned __int128)((unsigned __int128)(((unsigned __int128)((((unsigned __int128)UINT64_C(0x0) << 64) | (unsigned __int128)UINT64_C(0x0))) << 6) | (unsigned __int128)(((uint32_t)((uint32_t)c >> 0) & UINT32_C(0x3f))))))) >> 0)) : (uint64_t)((uint64_t)((uint64_t)((uint64_t)b) >> (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((uint32_t)((uint32_t)c >> 0) & UINT32_C(0x3f))))))))) : (uint64_t)(UINT64_C(0x0))));
}
