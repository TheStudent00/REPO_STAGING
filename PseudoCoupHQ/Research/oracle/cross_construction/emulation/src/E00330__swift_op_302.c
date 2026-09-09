/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E00330__swift_op_302.  The term's layer-5 text, LITERAL:
   If(0 <= v0, 0, 1) | If(ULE(v1, v0), 0, 1) */
#include <stdint.h>

uint8_t
emu_E00330__swift_op_302(uint64_t a, uint64_t b, uint64_t c)
{
    return (uint8_t)(((uint32_t)((uint32_t)(((((int64_t)(UINT64_C(0x0)) <= (int64_t)((uint64_t)a))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1)))) | (uint32_t)(((((uint64_t)((uint64_t)b) <= (uint64_t)((uint64_t)a))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1))))) & UINT32_C(0xff)));
}
