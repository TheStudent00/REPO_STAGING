/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of shr_imm_gpr_64__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(63, 3, v0)) */
#include <cstdint>

extern "C"
uint64_t
emu_shr_imm_gpr_64__reg_rdi__cpp(uint64_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 61) | (uint64_t)(((uint64_t)((uint64_t)a >> 3) & UINT64_C(0x1fffffffffffffff)))));
}
