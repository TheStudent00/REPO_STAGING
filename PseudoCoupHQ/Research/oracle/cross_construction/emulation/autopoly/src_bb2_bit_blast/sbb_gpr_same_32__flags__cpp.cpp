/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of sbb_gpr_same_32__flags__cpp.  The term's layer-5 text, LITERAL:
   Concat(Extract(31, 0, v0), Extract(31, 0, v0)) */
#include <cstdint>

extern "C"
uint64_t
emu_sbb_gpr_same_32__flags__cpp(uint32_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)((uint32_t)a) << 32) | (uint64_t)((uint32_t)a)));
}
