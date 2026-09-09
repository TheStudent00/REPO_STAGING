/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E00264__rust_op_281.  The term's layer-5 text, LITERAL:
   1 ^ Extract(7, 0, v0) ^ Extract(7, 0, v1) */
#include <stdint.h>

uint8_t
emu_E00264__rust_op_281(uint8_t a, uint8_t b)
{
    return (uint8_t)(((uint32_t)((uint32_t)((uint32_t)a) ^ (uint32_t)((uint32_t)b) ^ (uint32_t)(UINT32_C(0x1))) & UINT32_C(0xff)));
}
