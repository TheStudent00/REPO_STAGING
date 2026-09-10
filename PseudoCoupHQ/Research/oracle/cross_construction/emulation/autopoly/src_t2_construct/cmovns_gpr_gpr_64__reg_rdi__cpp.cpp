/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of cmovns_gpr_gpr_64__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   If(0 <= ~(~Extract(63, 0, v0) | ~v1), v2, v3) */
#include <cstdint>

extern "C"
uint64_t
emu_cmovns_gpr_gpr_64__reg_rdi__cpp(uint64_t a, uint64_t b, uint64_t c, uint64_t d)
{
    return (uint64_t)(((((int64_t)(UINT64_C(0x0)) <= (int64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)((uint64_t)(~(uint64_t)((uint64_t)b))) | (uint64_t)((uint64_t)(~(uint64_t)((uint64_t)a))))))))) ? (uint64_t)((uint64_t)c) : (uint64_t)((uint64_t)d)));
}
