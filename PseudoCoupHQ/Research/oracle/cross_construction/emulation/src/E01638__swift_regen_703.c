/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01638__swift_regen_703.  The term's layer-5 text, LITERAL:
   If(Extract(15, 0, v0) <= 0, 1, 0) | If(ULE(Extract(31, 0, v0), Extract(31, 0, v1)), 1, 0) */
#include <stdint.h>

uint8_t
emu_E01638__swift_regen_703(uint32_t a, uint32_t b, uint64_t c)
{
    return (uint8_t)(((uint32_t)((uint32_t)((((((int32_t)((uint32_t)(((uint32_t)((uint32_t)a >> 0) & UINT32_C(0xffff))) << 16) >> 16) <= ((int32_t)((uint32_t)(UINT32_C(0x0)) << 16) >> 16))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0)))) | (uint32_t)(((((uint32_t)((uint32_t)a) <= (uint32_t)((uint32_t)b))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0))))) & UINT32_C(0xff)));
}
