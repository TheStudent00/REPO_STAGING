/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01630__swift_regen_472.  The term's layer-5 text, LITERAL:
   ~(If(Extract(15, 0, v0) <= 0, 255, 254) | If(ULE(Extract(15, 0, v0), Extract(15, 0, v1)), 255, 254)) */
#include <stdint.h>

uint8_t
emu_E01630__swift_regen_472(uint16_t a, uint16_t b, uint64_t c)
{
    return (uint8_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)((((((int32_t)((uint32_t)((uint32_t)b) << 16) >> 16) <= ((int32_t)((uint32_t)(UINT32_C(0x0)) << 16) >> 16))) ? (uint32_t)(UINT32_C(0xff)) : (uint32_t)(UINT32_C(0xfe)))) | (uint32_t)(((((uint32_t)((uint32_t)b) <= (uint32_t)((uint32_t)a))) ? (uint32_t)(UINT32_C(0xff)) : (uint32_t)(UINT32_C(0xfe))))) & UINT32_C(0xff)))) & UINT32_C(0xff)));
}
