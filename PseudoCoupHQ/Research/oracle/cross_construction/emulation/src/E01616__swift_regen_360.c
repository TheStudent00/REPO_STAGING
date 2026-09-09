/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01616__swift_regen_360.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(15, 0, v0) + 65535*Extract(15, 0, v1)) */
#include <stdint.h>

uint32_t
emu_E01616__swift_regen_360(uint16_t a, uint16_t b)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)((uint32_t)b) * (uint32_t)(UINT32_C(0xffff))) & UINT32_C(0xffff))) + (uint32_t)((uint32_t)a)) & UINT32_C(0xffff)))));
}
