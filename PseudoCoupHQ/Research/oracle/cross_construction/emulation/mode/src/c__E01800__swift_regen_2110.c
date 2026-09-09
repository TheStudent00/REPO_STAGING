/* task o13 emulation WITH THE MODE -- rendered by mode.py ModeRendererC from the layer-4 term
   of c__E01800__swift_regen_2110, and from the guard the reference read off the x unit's own body.
   The term's layer-5 text, LITERAL:
   If(Or(Not(Extract(15, 8, v0) == 0), ULE(128, Extract(7, 0, v0))), 0, If(Extract(6, 6, v0) == 0, Extract(63, 0, LShR(Concat(v1, v2), Concat(0, Extract(5, 0, v0)))), LShR(v1, Concat(0, Extract(5, 0, v0))))) */
#include <stdint.h>

uint64_t
emu_c__E01800__swift_regen_2110(uint64_t a, uint64_t b, uint16_t c)
{
    return (uint64_t)(((((((uint32_t)(UINT32_C(0x80)) <= (uint32_t)(((uint32_t)((uint32_t)c >> 0) & UINT32_C(0xff))))) || ((!(((uint32_t)(((uint32_t)((uint32_t)c >> 8) & UINT32_C(0xff))) == (uint32_t)(UINT32_C(0x0)))))))) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)(((((uint32_t)(((uint32_t)((uint32_t)c >> 6) & UINT32_C(0x1))) == (uint32_t)(UINT32_C(0x0)))) ? (uint64_t)((uint64_t)((unsigned __int128)((unsigned __int128)((unsigned __int128)((unsigned __int128)(((unsigned __int128)((uint64_t)b) << 64) | (unsigned __int128)((uint64_t)a))) >> (unsigned)(unsigned __int128)((unsigned __int128)(((unsigned __int128)((((unsigned __int128)UINT64_C(0x0) << 64) | (unsigned __int128)UINT64_C(0x0))) << 6) | (unsigned __int128)(((uint32_t)((uint32_t)c >> 0) & UINT32_C(0x3f))))))) >> 0)) : (uint64_t)((uint64_t)((uint64_t)((uint64_t)b) >> (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((uint32_t)((uint32_t)c >> 0) & UINT32_C(0x3f)))))))))));
}
