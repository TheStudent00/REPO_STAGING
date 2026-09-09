/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01646__swift_regen_768.  The term's layer-5 text, LITERAL:
   ~(If(0 <= Extract(15, 0, v0), 254, 255) | If(ULE(Extract(15, 0, v1), Extract(15, 0, v0)), 254, 255)) */
#include <stdint.h>

uint8_t
emu_E01646__swift_regen_768(uint16_t a, uint16_t b, uint64_t c)
{
    return (uint8_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)((((((int32_t)((uint32_t)(UINT32_C(0x0)) << 16) >> 16) <= ((int32_t)((uint32_t)((uint32_t)b) << 16) >> 16))) ? (uint32_t)(UINT32_C(0xfe)) : (uint32_t)(UINT32_C(0xff)))) | (uint32_t)(((((uint32_t)((uint32_t)a) <= (uint32_t)((uint32_t)b))) ? (uint32_t)(UINT32_C(0xfe)) : (uint32_t)(UINT32_C(0xff))))) & UINT32_C(0xff)))) & UINT32_C(0xff)));
}
