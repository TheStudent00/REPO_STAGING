/* task o13 emulation WITH THE MODE -- rendered by mode.py ModeRendererC from the layer-4 term
   of c__E01593__swift_regen_325, and from the guard the reference read off the x unit's own body.
   The term's layer-5 text, LITERAL:
   Concat(0, Extract(7, 0, bvurem_i(Concat(0, Extract(7, 0, v0)), Concat(0, Extract(7, 0, v1)))), Extract(7, 0, bvudiv_i(Concat(0, Extract(7, 0, v0)), Concat(0, Extract(7, 0, v1))))) */
#include <stdint.h>

uint32_t
emu_c__E01593__swift_regen_325(uint8_t a, uint8_t b)
{
    if (((1) && (((uint32_t)(UINT32_C(0x0)) == (uint32_t)(((uint32_t)((uint32_t)((uint32_t)b) & (uint32_t)((uint32_t)b)) & UINT32_C(0xff))))))) { __builtin_trap(); }
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | ((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)((uint32_t)a)) & UINT32_C(0xffff))) % (uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)((uint32_t)b)) & UINT32_C(0xffff)))) & UINT32_C(0xffff))) >> 0) & UINT32_C(0xff))) << 8) | (uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)((uint32_t)a)) & UINT32_C(0xffff))) / (uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)((uint32_t)b)) & UINT32_C(0xffff)))) & UINT32_C(0xffff))) >> 0) & UINT32_C(0xff)))));
}
