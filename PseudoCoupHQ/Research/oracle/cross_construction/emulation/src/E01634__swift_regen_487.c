/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01634__swift_regen_487.  The term's layer-5 text, LITERAL:
   ~(If(Extract(7, 0, v0) <= 0, 255, 254) | If(ULE(Extract(31, 0, v0), Extract(31, 0, v1)), 255, 254)) */
#include <stdint.h>

uint8_t
emu_E01634__swift_regen_487(uint32_t a, uint32_t b, uint64_t c)
{
    return (uint8_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)((((((int32_t)((uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0xff))) << 24) >> 24) <= ((int32_t)((uint32_t)(UINT32_C(0x0)) << 24) >> 24))) ? (uint32_t)(UINT32_C(0xff)) : (uint32_t)(UINT32_C(0xfe)))) | (uint32_t)(((((uint32_t)((uint32_t)b) <= (uint32_t)((uint32_t)a))) ? (uint32_t)(UINT32_C(0xff)) : (uint32_t)(UINT32_C(0xfe))))) & UINT32_C(0xff)))) & UINT32_C(0xff)));
}
