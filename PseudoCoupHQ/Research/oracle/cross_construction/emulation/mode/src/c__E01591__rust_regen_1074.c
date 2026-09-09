/* task o13 emulation WITH THE MODE -- rendered by mode.py ModeRendererC from the layer-4 term
   of c__E01591__rust_regen_1074, and from the guard the reference read off the x unit's own body.
   The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 16, v0), Extract(15, 0, bvudiv_i(Concat(0, Extract(15, 0, v0)), Concat(0, Extract(15, 0, v1))))) */
#include <stdint.h>
void _RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero(void) __attribute__((noreturn));

uint64_t
emu_c__E01591__rust_regen_1074(uint32_t a, uint16_t b, uint64_t c)
{
    if (((1) && (((uint32_t)(UINT32_C(0x0)) == (uint32_t)(((uint32_t)((uint32_t)((uint32_t)b) & (uint32_t)((uint32_t)b)) & UINT32_C(0xffff))))))) { _RNvNtNtCs3BFokC4QLxY_4core9panicking11panic_const23panic_const_div_by_zero(); }
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | ((uint64_t)(((uint32_t)((uint32_t)a >> 16) & UINT32_C(0xffff))) << 16) | (uint64_t)(((uint32_t)((uint32_t)((uint32_t)((uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)(((uint32_t)((uint32_t)a >> 0) & UINT32_C(0xffff))))) / (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)((uint32_t)b))))) >> 0) & UINT32_C(0xffff)))));
}
