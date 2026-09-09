/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E00342__swift_op_523.  The term's layer-5 text, LITERAL:
   ~(If(v0 == v1, 254, 255) | If(0 <= v1, 254, 255)) */
#include <stdint.h>

uint8_t
emu_E00342__swift_op_523(uint64_t a, uint64_t b, uint64_t c)
{
    return (uint8_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((((uint64_t)((uint64_t)a) == (uint64_t)((uint64_t)b))) ? (uint32_t)(UINT32_C(0xfe)) : (uint32_t)(UINT32_C(0xff)))) | (uint32_t)(((((int64_t)(UINT64_C(0x0)) <= (int64_t)((uint64_t)b))) ? (uint32_t)(UINT32_C(0xfe)) : (uint32_t)(UINT32_C(0xff))))) & UINT32_C(0xff)))) & UINT32_C(0xff)));
}
