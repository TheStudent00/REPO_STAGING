/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01810__swift_regen_2123.  The term's layer-5 text, LITERAL:
   If(Or(Not(Extract(31, 5, v0) == 0), ULE(16, Extract(4, 0, v0))), 0, LShR(Concat(0, Extract(15, 0, v1)), Concat(0, Extract(3, 0, v0)))) */
#include <stdint.h>

uint32_t
emu_E01810__swift_regen_2123(uint16_t a, uint32_t b)
{
    return (uint32_t)(((((((uint32_t)(UINT32_C(0x10)) <= (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f))))) || ((!(((uint32_t)(((uint32_t)((uint32_t)b >> 5) & UINT32_C(0x7ffffff))) == (uint32_t)(UINT32_C(0x0)))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)((uint32_t)((uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)((uint32_t)a))) >> (unsigned)(uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 4) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0xf)))))))));
}
