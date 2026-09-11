/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of setae_gpr_one_8__reg_rdi__c__native_first.  The term's text, LITERAL:
   Concat(Extract(63, 8, v0), If(ULE(Extract(7, 0, v1), Extract(7, 0, v2)), 1, 0)) */
#include <stdint.h>

uint64_t
emu_setae_gpr_one_8__reg_rdi__c__native_first(uint8_t a, uint8_t b, uint64_t c)
{
    uint32_t v0 = (uint32_t)a;
    uint32_t v1 = (uint32_t)b;
    int v2 = (((uint32_t)(v1) <= (uint32_t)(v0))) ? 1 : 0;
    uint32_t v3 = ((v2) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0)));
    uint64_t v4 = ((uint64_t)((uint64_t)c >> 8) & UINT64_C(0xffffffffffffff));
    uint64_t v5 = (uint64_t)(((uint64_t)(v4) << 8) | (uint64_t)(v3));
    return (uint64_t)(v5);
}
