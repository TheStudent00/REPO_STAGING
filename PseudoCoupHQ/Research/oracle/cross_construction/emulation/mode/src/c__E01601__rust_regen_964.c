/* task o13 emulation WITH THE MODE -- rendered by mode.py ModeRendererC from the layer-4 term
   of c__E01601__rust_regen_964, and from the guard the reference read off the x unit's own body.
   The term's layer-5 text, LITERAL:
   LShR(Concat(0, Extract(15, 0, v0)), Concat(0, Extract(3, 0, v1))) */
#include <stdint.h>

uint32_t
emu_c__E01601__rust_regen_964(uint16_t a, uint8_t b)
{
    return (uint32_t)((uint32_t)((uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)((uint32_t)a))) >> (unsigned)(uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 4) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0xf)))))));
}
