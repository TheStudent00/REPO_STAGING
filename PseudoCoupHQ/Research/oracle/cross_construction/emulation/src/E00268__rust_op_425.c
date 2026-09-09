/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E00268__rust_op_425.  The term's layer-5 text, LITERAL:
   Concat(~(~Extract(7, 1, v0) | ~Extract(7, 1, v1)), ~(Extract(0, 0, v1) | ~Extract(0, 0, v0))) */
#include <stdint.h>

uint8_t
emu_E00268__rust_op_425(uint8_t a, uint8_t b)
{
    return (uint8_t)(((uint32_t)(((uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)a >> 1) & UINT32_C(0x7f)))) & UINT32_C(0x7f))) | (uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)b >> 1) & UINT32_C(0x7f)))) & UINT32_C(0x7f)))) & UINT32_C(0x7f)))) & UINT32_C(0x7f))) << 1) | (uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)a >> 0) & UINT32_C(0x1)))) & UINT32_C(0x1))) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1)))) & UINT32_C(0x1)))) & UINT32_C(0x1)))) & UINT32_C(0xff)));
}
