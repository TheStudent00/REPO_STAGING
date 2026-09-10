/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of shl_imm_gpr_64__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   Concat(Extract(60, 0, v0), 0) */
#include <cstdint>

extern "C"
uint64_t
emu_shl_imm_gpr_64__reg_rdi__cpp(uint64_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)(((uint64_t)((uint64_t)a >> 0) & UINT64_C(0x1fffffffffffffff))) << 3) | (uint64_t)(UINT32_C(0x0))));
}
