/* task o13 emulation WITH THE MODE -- rendered by mode.py ModeRendererC from the layer-4 term
   of c__E01532__go_regen_146, and from the guard the reference read off the x unit's own body.
   The term's layer-5 text, LITERAL:
   Concat(0, Extract(15, 0, bvudiv_i(Concat(0, Extract(7, 0, v0)), Concat(0, Extract(7, 0, v1))))) */
#include <stdint.h>
void runtime_panicdivide(void) __attribute__((noreturn));

uint32_t
emu_c__E01532__go_regen_146(uint8_t a, uint8_t b)
{
    if (((1) && (((uint32_t)(UINT32_C(0x0)) == (uint32_t)(((uint32_t)((uint32_t)((uint32_t)b) & (uint32_t)((uint32_t)b)) & UINT32_C(0xff))))))) { runtime_panicdivide(); }
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)(((uint32_t)((uint32_t)((uint32_t)((uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)((uint32_t)a))) / (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)((uint32_t)b))))) >> 0) & UINT32_C(0xffff)))));
}
