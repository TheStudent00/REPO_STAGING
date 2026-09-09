/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of xor_imm_gpr_32__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 2, v0), ~Extract(1, 0, v0)) */
#include <cstdint>

extern "C"
uint64_t
emu_xor_imm_gpr_32__reg_rdi__cpp(uint32_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | ((uint64_t)(((uint32_t)((uint32_t)a >> 2) & UINT32_C(0x3fffffff))) << 2) | (uint64_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)a >> 0) & UINT32_C(0x3)))) & UINT32_C(0x3)))));
}
