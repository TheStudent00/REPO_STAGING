/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01617__swift_regen_363.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(7, 0, v0) + 255*Extract(7, 0, v1)) */
#include <stdint.h>

uint32_t
emu_E01617__swift_regen_363(uint8_t a, uint8_t b)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)((uint32_t)b) * (uint32_t)(UINT32_C(0xff))) & UINT32_C(0xff))) + (uint32_t)((uint32_t)a)) & UINT32_C(0xff)))));
}
