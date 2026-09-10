/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of mulhu_gpr_gpr_same_64__reg_a0__c.  The term's layer-5 text, LITERAL:
   Extract(127, 64, Concat(0, v0)*Concat(0, v0)) */
#include <stdint.h>

uint64_t
emu_mulhu_gpr_gpr_same_64__reg_a0__c(uint64_t a)
{
    return (uint64_t)((uint64_t)((unsigned __int128)((unsigned __int128)((unsigned __int128)((unsigned __int128)(((unsigned __int128)(UINT64_C(0x0)) << 64) | (unsigned __int128)((uint64_t)a))) * (unsigned __int128)((unsigned __int128)(((unsigned __int128)(UINT64_C(0x0)) << 64) | (unsigned __int128)((uint64_t)a))))) >> 64));
}
