/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01619__swift_regen_43.  The term's layer-5 text, LITERAL:
   Concat(0, 255*Extract(7, 0, v0)) */
#include <stdint.h>

uint32_t
emu_E01619__swift_regen_43(uint8_t a)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)(((uint32_t)((uint32_t)((uint32_t)a) * (uint32_t)(UINT32_C(0xff))) & UINT32_C(0xff)))));
}
