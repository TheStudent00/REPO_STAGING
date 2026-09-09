/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01781__swift_regen_2085.  The term's layer-5 text, LITERAL:
   Extract(7, 0, v0) >> 7 */
#include <stdint.h>

uint8_t
emu_E01781__swift_regen_2085(uint8_t a, uint64_t b, uint64_t c)
{
    return (uint8_t)(((uint32_t)(((int32_t)((uint32_t)((uint32_t)a) << 24) >> 24) >> (unsigned)(uint32_t)(UINT32_C(0x7))) & UINT32_C(0xff)));
}
