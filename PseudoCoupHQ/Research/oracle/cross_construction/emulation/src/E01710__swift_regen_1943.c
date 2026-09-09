/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01710__swift_regen_1943.  The term's layer-5 text, LITERAL:
   If(Or(Not(Extract(31, 4, v0) == 0), ULE(8, Extract(3, 0, v0))), 0, Concat(0, Extract(7, 0, v1) << Concat(0, Extract(2, 0, v0)))) */
#include <stdint.h>

uint32_t
emu_E01710__swift_regen_1943(uint8_t a, uint32_t b)
{
    return (uint32_t)(((((((uint32_t)(UINT32_C(0x8)) <= (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0xf))))) || ((!(((uint32_t)(((uint32_t)((uint32_t)b >> 4) & UINT32_C(0xfffffff))) == (uint32_t)(UINT32_C(0x0)))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)(((uint32_t)((uint32_t)((uint32_t)a) << (unsigned)(uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 3) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x7)))) & UINT32_C(0xff)))) & UINT32_C(0xff)))))));
}
