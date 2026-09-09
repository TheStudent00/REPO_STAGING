/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of mul_gpr_one_64__reg_rax__cpp.  The term's layer-5 text, LITERAL:
   v0*v1 */
#include <cstdint>

extern "C"
uint64_t
emu_mul_gpr_one_64__reg_rax__cpp(uint64_t a, uint64_t b)
{
    return (uint64_t)((uint64_t)((uint64_t)((uint64_t)a) * (uint64_t)((uint64_t)b)));
}
