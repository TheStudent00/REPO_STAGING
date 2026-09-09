/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01585__rust_regen_1043.  The term's layer-5 text, LITERAL:
   Extract(7, 0, v0) + 255*Extract(7, 0, v1) */
#include <stdint.h>

uint8_t
emu_E01585__rust_regen_1043(uint8_t a, uint8_t b)
{
    return (uint8_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)((uint32_t)b) * (uint32_t)(UINT32_C(0xff))) & UINT32_C(0xff))) + (uint32_t)((uint32_t)a)) & UINT32_C(0xff)));
}
