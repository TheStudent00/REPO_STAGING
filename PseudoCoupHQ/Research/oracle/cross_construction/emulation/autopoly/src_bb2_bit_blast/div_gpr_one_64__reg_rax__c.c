/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of div_gpr_one_64__reg_rax__c.  The term's layer-5 text, LITERAL:
   Extract(63, 0, bvudiv_i(Concat(v0, v1), Concat(0, v2))) */
#include <stdint.h>

uint64_t
emu_div_gpr_one_64__reg_rax__c(uint64_t a, uint64_t b, uint64_t c)
{
    return (uint64_t)((uint64_t)((unsigned __int128)((unsigned __int128)((unsigned __int128)((unsigned __int128)(((unsigned __int128)((uint64_t)a) << 64) | (unsigned __int128)((uint64_t)b))) / (unsigned __int128)((unsigned __int128)(((unsigned __int128)(UINT64_C(0x0)) << 64) | (unsigned __int128)((uint64_t)c))))) >> 0));
}
