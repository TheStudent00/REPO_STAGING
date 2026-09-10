/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of mul_gpr_one_64__reg_rdx__c.  The term's layer-5 text, LITERAL:
   Extract(127, 64, Concat(0, v0)*Concat(0, v1)) */
#include <stdint.h>

uint64_t
emu_mul_gpr_one_64__reg_rdx__c(uint64_t a, uint64_t b)
{
    return (uint64_t)((uint64_t)((unsigned __int128)((unsigned __int128)((unsigned __int128)((unsigned __int128)(((unsigned __int128)(UINT64_C(0x0)) << 64) | (unsigned __int128)((uint64_t)a))) * (unsigned __int128)((unsigned __int128)(((unsigned __int128)(UINT64_C(0x0)) << 64) | (unsigned __int128)((uint64_t)b))))) >> 64));
}
