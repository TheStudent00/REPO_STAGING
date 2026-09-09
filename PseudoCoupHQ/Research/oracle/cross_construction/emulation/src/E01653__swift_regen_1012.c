/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01653__swift_regen_1012.  The term's layer-5 text, LITERAL:
   If(Extract(31, 0, v0) == Extract(31, 0, v1), 0, 1) | If(0 <= Extract(31, 0, v0), 0, 1) */
#include <stdint.h>

uint8_t
emu_E01653__swift_regen_1012(uint32_t a, uint32_t b, uint64_t c)
{
    return (uint8_t)(((uint32_t)((uint32_t)(((((uint32_t)((uint32_t)a) == (uint32_t)((uint32_t)b))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1)))) | (uint32_t)(((((int32_t)(UINT32_C(0x0)) <= (int32_t)((uint32_t)a))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1))))) & UINT32_C(0xff)));
}
