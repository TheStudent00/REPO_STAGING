/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E00332__swift_op_307.  The term's layer-5 text, LITERAL:
   ~(If(v0 <= 0, 255, 254) | If(ULE(v0, v1), 255, 254)) */
#include <stdint.h>

uint8_t
emu_E00332__swift_op_307(uint64_t a, uint64_t b, uint64_t c)
{
    return (uint8_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((((int64_t)((uint64_t)b) <= (int64_t)(UINT64_C(0x0)))) ? (uint32_t)(UINT32_C(0xff)) : (uint32_t)(UINT32_C(0xfe)))) | (uint32_t)(((((uint64_t)((uint64_t)b) <= (uint64_t)((uint64_t)a))) ? (uint32_t)(UINT32_C(0xff)) : (uint32_t)(UINT32_C(0xfe))))) & UINT32_C(0xff)))) & UINT32_C(0xff)));
}
