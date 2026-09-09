/* task o13 emulation WITH THE MODE -- rendered by mode.py ModeRendererC from the layer-4 term
   of c__E01831__swift_regen_2633, and from the guard the reference read off the x unit's own body.
   The term's layer-5 text, LITERAL:
   Concat(0, Extract(7, 0, v0), Extract(7, 0, v1)) */
#include <stdint.h>

uint32_t
emu_c__E01831__swift_regen_2633(uint8_t a, uint8_t b)
{
    if (((1) && ((((int32_t)((uint32_t)((uint32_t)b) << 24) >> 24) < ((int32_t)((uint32_t)((uint32_t)a) << 24) >> 24))))) { __builtin_trap(); }
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | ((uint32_t)((uint32_t)b) << 8) | (uint32_t)((uint32_t)a)));
}
