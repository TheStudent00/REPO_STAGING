/* task ex1 emulation -- rendered by cpp_render.py CppRenderer from the layer-4 term of shld_cl_gpr_gpr_64__reg_rdi__cpp.  The term's layer-5 text, LITERAL:
   Extract(127, 64, Concat(v0, v1) << Concat(0, Extract(5, 0, v2))) */
#include <cstdint>

extern "C"
uint64_t
emu_shld_cl_gpr_gpr_64__reg_rdi__cpp(uint64_t a, uint64_t b, uint8_t c)
{
    return (uint64_t)((uint64_t)((unsigned __int128)((unsigned __int128)((unsigned __int128)((unsigned __int128)(((unsigned __int128)((uint64_t)a) << 64) | (unsigned __int128)((uint64_t)b))) << (unsigned)(unsigned __int128)((unsigned __int128)(((unsigned __int128)((((unsigned __int128)UINT64_C(0x0) << 64) | (unsigned __int128)UINT64_C(0x0))) << 6) | (unsigned __int128)(((uint32_t)((uint32_t)c >> 0) & UINT32_C(0x3f))))))) >> 64));
}
