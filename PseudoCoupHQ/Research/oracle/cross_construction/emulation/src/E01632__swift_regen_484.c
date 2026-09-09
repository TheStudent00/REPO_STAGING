/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01632__swift_regen_484.  The term's layer-5 text, LITERAL:
   ~(If(Extract(15, 0, v0) <= 0, 255, 254) | If(ULE(Extract(31, 0, v0), Extract(31, 0, v1)), 255, 254)) */
#include <stdint.h>

uint8_t
emu_E01632__swift_regen_484(uint32_t a, uint32_t b, uint64_t c)
{
    return (uint8_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)((((((int32_t)((uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0xffff))) << 16) >> 16) <= ((int32_t)((uint32_t)(UINT32_C(0x0)) << 16) >> 16))) ? (uint32_t)(UINT32_C(0xff)) : (uint32_t)(UINT32_C(0xfe)))) | (uint32_t)(((((uint32_t)((uint32_t)b) <= (uint32_t)((uint32_t)a))) ? (uint32_t)(UINT32_C(0xff)) : (uint32_t)(UINT32_C(0xfe))))) & UINT32_C(0xff)))) & UINT32_C(0xff)));
}
