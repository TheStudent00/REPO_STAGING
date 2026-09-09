/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E00338__swift_op_446.  The term's layer-5 text, LITERAL:
   If(v0 == v1, 0, 1) | If(0 <= v0, 0, 1) */
#include <stdint.h>

uint8_t
emu_E00338__swift_op_446(uint64_t a, uint64_t b, uint64_t c)
{
    return (uint8_t)(((uint32_t)((uint32_t)(((((uint64_t)((uint64_t)a) == (uint64_t)((uint64_t)b))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1)))) | (uint32_t)(((((int64_t)(UINT64_C(0x0)) <= (int64_t)((uint64_t)a))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1))))) & UINT32_C(0xff)));
}
