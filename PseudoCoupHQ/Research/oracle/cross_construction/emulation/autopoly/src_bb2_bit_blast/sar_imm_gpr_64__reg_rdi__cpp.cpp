/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of sar_imm_gpr_64__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   v0 >> 3 */
#include <cstdint>

extern "C"
uint64_t
emu_sar_imm_gpr_64__reg_rdi__cpp(uint64_t a)
{
    return (uint64_t)((uint64_t)((int64_t)((uint64_t)a) >> (unsigned)(uint64_t)(UINT64_C(0x3))));
}
