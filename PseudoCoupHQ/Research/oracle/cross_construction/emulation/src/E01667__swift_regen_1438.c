/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01667__swift_regen_1438.  The term's layer-5 text, LITERAL:
   ~(If(Extract(31, 0, v0) == Extract(31, 0, v1), 254, 255) | If(0 <= Extract(15, 0, v0), 254, 255)) */
#include <stdint.h>

uint8_t
emu_E01667__swift_regen_1438(uint32_t a, uint32_t b, uint64_t c)
{
    return (uint8_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((((uint32_t)((uint32_t)a) == (uint32_t)((uint32_t)b))) ? (uint32_t)(UINT32_C(0xfe)) : (uint32_t)(UINT32_C(0xff)))) | (uint32_t)((((((int32_t)((uint32_t)(UINT32_C(0x0)) << 16) >> 16) <= ((int32_t)((uint32_t)(((uint32_t)((uint32_t)a >> 0) & UINT32_C(0xffff))) << 16) >> 16))) ? (uint32_t)(UINT32_C(0xfe)) : (uint32_t)(UINT32_C(0xff))))) & UINT32_C(0xff)))) & UINT32_C(0xff)));
}
