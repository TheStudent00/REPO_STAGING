/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of xor_imm_gpr_32__flags__cpp.  The term's layer-5 text, LITERAL:
   Concat(Extract(31, 0, v0) ^ Extract(31, 0, v1), 0) */
#include <cstdint>

extern "C"
uint64_t
emu_xor_imm_gpr_32__flags__cpp(uint32_t a, uint32_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)((uint32_t)((uint32_t)((uint32_t)b) ^ (uint32_t)((uint32_t)a))) << 32) | (uint64_t)(UINT32_C(0x0))));
}
