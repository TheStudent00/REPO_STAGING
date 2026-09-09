/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of cpp_79__cpp_regen_24890.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 32, v0), Extract(31, 0, v0) ^ Extract(31, 0, v1)) */
#include <stdint.h>

uint64_t
emu_cpp_79__cpp_regen_24890(uint64_t a, uint64_t b, uint32_t c)
{
    return (uint64_t)((uint64_t)(((uint64_t)((uint32_t)((uint64_t)a >> 32)) << 32) | (uint64_t)((uint32_t)((uint32_t)((uint32_t)((uint64_t)a >> 0)) ^ (uint32_t)((uint32_t)c)))));
}
