/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of cpp_69__cpp_op_149.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 0, v0))*18446744073709551615 + v1 */
#include <stdint.h>

uint64_t
emu_cpp_69__cpp_op_149(uint64_t a, uint32_t b)
{
    return (uint64_t)((uint64_t)((uint64_t)((uint64_t)((uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)b))) * (uint64_t)(UINT64_C(0xffffffffffffffff)))) + (uint64_t)((uint64_t)a)));
}
