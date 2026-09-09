/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of go_24__go_op_17.  The term's layer-5 text, LITERAL:
   Concat(Extract(31, 1, v0), ~Extract(0, 0, v0)) */
#include <stdint.h>

uint32_t
emu_go_24__go_op_17(uint32_t a)
{
    return (uint32_t)((uint32_t)(((uint32_t)(((uint32_t)((uint32_t)a >> 1) & UINT32_C(0x7fffffff))) << 1) | (uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)a >> 0) & UINT32_C(0x1)))) & UINT32_C(0x1)))));
}
