/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E00321__rust_op_821.  The term's layer-5 text, LITERAL:
   Extract(31, 0, v0) + Concat(Extract(23, 0, v1), 0) */
#include <stdint.h>

uint32_t
emu_E00321__rust_op_821(uint32_t a, uint32_t b)
{
    return (uint32_t)((uint32_t)((uint32_t)((uint32_t)(((uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0xffffff))) << 8) | (uint32_t)(UINT32_C(0x0)))) + (uint32_t)((uint32_t)a)));
}
