/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of cpp_60__cpp_op_679.  The term's layer-5 text, LITERAL:
   Extract(31, 0, v0) << Concat(0, Extract(4, 0, v1)) */
#include <stdint.h>

uint32_t
emu_cpp_60__cpp_op_679(uint32_t a, uint8_t b)
{
    return (uint32_t)((uint32_t)((uint32_t)((uint32_t)a) << (unsigned)(uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))))));
}
