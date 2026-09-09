/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01563__go_regen_385.  The term's layer-5 text, LITERAL:
   Concat(0, ~(~LShR(Extract(7, 0, v0), Concat(0, Extract(4, 0, v1))) | ~(255*If(Or(Not(Extract(15, 4, v1) == 0), ULE(8, Extract(3, 0, v1))), 0, 1)))) */
#include <stdint.h>

uint32_t
emu_E01563__go_regen_385(uint8_t a, uint16_t b)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)((((uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0xff))) < (uint32_t)8) ? ((uint32_t)((uint32_t)((uint32_t)a) >> (unsigned)(uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0xff)))) & UINT32_C(0xff)) : (uint32_t)0))) & UINT32_C(0xff))) | (uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((((((uint32_t)(UINT32_C(0x8)) <= (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0xf))))) || ((!(((uint32_t)(((uint32_t)((uint32_t)b >> 4) & UINT32_C(0xfff))) == (uint32_t)(UINT32_C(0x0)))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1)))) * (uint32_t)(UINT32_C(0xff))) & UINT32_C(0xff)))) & UINT32_C(0xff)))) & UINT32_C(0xff)))) & UINT32_C(0xff)))));
}
