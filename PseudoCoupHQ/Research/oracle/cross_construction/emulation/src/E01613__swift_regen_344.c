/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01613__swift_regen_344.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(15, 0, v0) + Extract(15, 0, v1)) */
#include <stdint.h>

uint32_t
emu_E01613__swift_regen_344(uint16_t a, uint16_t b)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)(((uint32_t)((uint32_t)((uint32_t)a) + (uint32_t)((uint32_t)b)) & UINT32_C(0xffff)))));
}
