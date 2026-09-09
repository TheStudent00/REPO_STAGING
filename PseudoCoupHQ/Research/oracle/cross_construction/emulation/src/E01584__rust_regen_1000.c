/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01584__rust_regen_1000.  The term's layer-5 text, LITERAL:
   LShR(Extract(7, 0, v0), Concat(0, Extract(2, 0, v1))) */
#include <stdint.h>

uint8_t
emu_E01584__rust_regen_1000(uint8_t a, uint8_t b)
{
    return (uint8_t)(((uint32_t)((uint32_t)((uint32_t)a) >> (unsigned)(uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 3) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x7)))) & UINT32_C(0xff)))) & UINT32_C(0xff)));
}
