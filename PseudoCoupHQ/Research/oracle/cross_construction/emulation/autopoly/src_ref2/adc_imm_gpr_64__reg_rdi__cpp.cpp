/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of adc_imm_gpr_64__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   If(Extract(64, 64, Concat(0, v0) + Concat(0, v1)) == 1, 1, 0) + v2 + v3 */
#include <cstdint>

extern "C"
uint64_t
emu_adc_imm_gpr_64__reg_rdi__cpp(uint64_t a, uint64_t b, uint64_t c, uint64_t d)
{
    return (uint64_t)((uint64_t)((uint64_t)(((((uint32_t)(((uint32_t)((unsigned __int128)(((unsigned __int128)((unsigned __int128)(((unsigned __int128)(((unsigned __int128)(UINT32_C(0x0)) << 64) | (unsigned __int128)((uint64_t)b)) & (((unsigned __int128)UINT64_C(0x1) << 64) | (unsigned __int128)UINT64_C(0xffffffffffffffff)))) + (unsigned __int128)(((unsigned __int128)(((unsigned __int128)(UINT32_C(0x0)) << 64) | (unsigned __int128)((uint64_t)a)) & (((unsigned __int128)UINT64_C(0x1) << 64) | (unsigned __int128)UINT64_C(0xffffffffffffffff))))) & (((unsigned __int128)UINT64_C(0x1) << 64) | (unsigned __int128)UINT64_C(0xffffffffffffffff)))) >> 64) & UINT32_C(0x1))) == (uint32_t)(UINT32_C(0x1)))) ? (uint64_t)(UINT64_C(0x1)) : (uint64_t)(UINT64_C(0x0)))) + (uint64_t)((uint64_t)d) + (uint64_t)((uint64_t)c)));
}
