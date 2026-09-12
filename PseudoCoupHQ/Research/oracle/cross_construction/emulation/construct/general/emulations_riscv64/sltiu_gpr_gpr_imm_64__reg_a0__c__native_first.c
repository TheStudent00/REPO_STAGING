/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of sltiu_gpr_gpr_imm_64__reg_a0__c__native_first.  The term's text, LITERAL:
   If(Or(Extract(1, 0, v0) == 3, Not(Extract(63, 2, v0) == 0)), 0, 1) */
#include <stdint.h>

uint64_t
emu_sltiu_gpr_gpr_imm_64__reg_a0__c__native_first(uint64_t a)
{
    uint64_t v0 = ((uint64_t)((uint64_t)a >> 2) & UINT64_C(0x3fffffffffffffff));
    int v1 = (((uint64_t)(v0) == (uint64_t)(UINT64_C(0x0)))) ? 1 : 0;
    int v2 = ((!(v1))) ? 1 : 0;
    uint32_t v3 = ((uint32_t)((uint64_t)a >> 0) & UINT32_C(0x3));
    int v4 = (((uint32_t)(v3) == (uint32_t)(UINT32_C(0x3)))) ? 1 : 0;
    int v5 = (((v4) || (v2))) ? 1 : 0;
    uint64_t v6 = ((v5) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)(UINT64_C(0x1)));
    return (uint64_t)(v6);
}
