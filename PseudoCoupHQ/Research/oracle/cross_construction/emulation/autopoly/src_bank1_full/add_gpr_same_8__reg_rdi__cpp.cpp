/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of add_gpr_same_8__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(7, 0, v0)*2) */
#include <cstdint>

extern "C"
uint64_t
emu_add_gpr_same_8__reg_rdi__cpp(uint8_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 8) | (uint64_t)(((uint32_t)((uint32_t)((uint32_t)a) * (uint32_t)(UINT32_C(0x2))) & UINT32_C(0xff)))));
}
