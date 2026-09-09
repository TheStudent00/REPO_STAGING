/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01664__swift_regen_1413.  The term's layer-5 text, LITERAL:
   If(Concat(0, Extract(31, 0, v0)) == v1, 1, 0) */
#include <stdint.h>

uint8_t
emu_E01664__swift_regen_1413(uint64_t a, uint32_t b)
{
    return (uint8_t)(((((uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)b))) == (uint64_t)((uint64_t)a))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0))));
}
