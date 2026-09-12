/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of setbe_gpr_one_8__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 8, v2), If(Or(Extract(7, 0, v0) == Extract(7, 0, v1), Not(ULE(Extract(7, 0, v0), Extract(7, 0, v1)))), 1, 0)) */
#include <cstdint>

extern "C"
uint64_t
emu_setbe_gpr_one_8__reg_rdi__cpp(uint8_t a, uint8_t b, uint64_t c)
{
    return (uint64_t)((uint64_t)(((uint64_t)(((uint64_t)((uint64_t)c >> 8) & UINT64_C(0xffffffffffffff))) << 8) | (uint64_t)(((((((uint32_t)((uint32_t)b) == (uint32_t)((uint32_t)a))) || ((!(((uint32_t)((uint32_t)b) <= (uint32_t)((uint32_t)a))))))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0))))));
}
