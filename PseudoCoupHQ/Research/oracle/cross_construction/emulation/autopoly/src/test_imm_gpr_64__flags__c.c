/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of test_imm_gpr_64__flags__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(1, 0, v0), 0) */
#include <stdint.h>

unsigned __int128
emu_test_imm_gpr_64__flags__c(uint8_t a)
{
    return (unsigned __int128)((unsigned __int128)(((unsigned __int128)(UINT64_C(0x0)) << 66) | ((unsigned __int128)(((uint32_t)((uint32_t)a >> 0) & UINT32_C(0x3))) << 64) | (unsigned __int128)(UINT64_C(0x0))));
}
