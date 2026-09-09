/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01618__swift_regen_40.  The term's layer-5 text, LITERAL:
   Concat(0, 65535*Extract(15, 0, v0)) */
#include <stdint.h>

uint32_t
emu_E01618__swift_regen_40(uint16_t a)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)(((uint32_t)((uint32_t)((uint32_t)a) * (uint32_t)(UINT32_C(0xffff))) & UINT32_C(0xffff)))));
}
