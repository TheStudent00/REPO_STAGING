/* task o13 emulation WITH THE MODE -- rendered by mode.py ModeRendererC from the layer-4 term
   of c__E01826__swift_regen_2156, and from the guard the reference read off the x unit's own body.
   The term's layer-5 text, LITERAL:
   If(Or(Not(Extract(63, 4, v0) == 0), ULE(8, Extract(3, 0, v0))), 0, Concat(0, LShR(Extract(7, 0, v1), Concat(0, Extract(2, 0, v0))))) */
#include <stdint.h>

uint32_t
emu_c__E01826__swift_regen_2156(uint8_t a, uint64_t b)
{
    return (uint32_t)(((((((uint32_t)(UINT32_C(0x8)) <= (uint32_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0xf))))) || ((!(((uint64_t)(((uint64_t)((uint64_t)b >> 4) & UINT64_C(0xfffffffffffffff))) == (uint64_t)(UINT64_C(0x0)))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)(((uint32_t)((uint32_t)((uint32_t)a) >> (unsigned)(uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 3) | (uint32_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x7)))) & UINT32_C(0xff)))) & UINT32_C(0xff)))))));
}
