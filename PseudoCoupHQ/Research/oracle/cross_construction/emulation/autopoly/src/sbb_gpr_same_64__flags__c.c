/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of sbb_gpr_same_64__flags__c.  The term's layer-5 text, LITERAL:
   Concat(v0, v0) */
#include <stdint.h>

unsigned __int128
emu_sbb_gpr_same_64__flags__c(uint64_t a)
{
    return (unsigned __int128)((unsigned __int128)(((unsigned __int128)((uint64_t)a) << 64) | (unsigned __int128)((uint64_t)a)));
}
