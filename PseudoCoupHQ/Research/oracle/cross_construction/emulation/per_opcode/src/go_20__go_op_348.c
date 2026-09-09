/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of go_20__go_op_348.  The term's layer-5 text, LITERAL:
   Extract(31, 0, v0)*4294967295 + Extract(31, 0, v1) */
#include <stdint.h>

uint32_t
emu_go_20__go_op_348(uint32_t a, uint32_t b)
{
    return (uint32_t)((uint32_t)((uint32_t)((uint32_t)((uint32_t)((uint32_t)b) * (uint32_t)(UINT32_C(0xffffffff)))) + (uint32_t)((uint32_t)a)));
}
