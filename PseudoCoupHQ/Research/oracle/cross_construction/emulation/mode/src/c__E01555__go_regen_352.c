/* task o13 emulation WITH THE MODE -- rendered by mode.py ModeRendererC from the layer-4 term
   of c__E01555__go_regen_352, and from the guard the reference read off the x unit's own body.
   The term's layer-5 text, LITERAL:
   Concat(0, ~(~LShR(Extract(15, 0, v0), Concat(0, Extract(4, 0, v1))) | ~(65535*If(Or(Not(Extract(15, 5, v1) == 0), ULE(16, Extract(4, 0, v1))), 0, 1)))) */
#include <stdint.h>

uint32_t
emu_c__E01555__go_regen_352(uint16_t a, uint16_t b)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)((((uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0xffff))) < (uint32_t)16) ? ((uint32_t)((uint32_t)((uint32_t)a) >> (unsigned)(uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0xffff)))) & UINT32_C(0xffff)) : (uint32_t)0))) & UINT32_C(0xffff))) | (uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((((((uint32_t)(UINT32_C(0x10)) <= (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f))))) || ((!(((uint32_t)(((uint32_t)((uint32_t)b >> 5) & UINT32_C(0x7ff))) == (uint32_t)(UINT32_C(0x0)))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1)))) * (uint32_t)(UINT32_C(0xffff))) & UINT32_C(0xffff)))) & UINT32_C(0xffff)))) & UINT32_C(0xffff)))) & UINT32_C(0xffff)))));
}
