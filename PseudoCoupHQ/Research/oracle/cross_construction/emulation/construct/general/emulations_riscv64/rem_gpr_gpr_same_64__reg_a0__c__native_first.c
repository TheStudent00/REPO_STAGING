/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of rem_gpr_gpr_same_64__reg_a0__c__native_first.  The term's text, LITERAL:
   If(v0 == 0, v0, If(And(v0 == 18446744073709551615, v0 == 9223372036854775808), 0, bvsrem_i(v0, v0))) */
#include <stdint.h>

uint64_t
emu_rem_gpr_gpr_same_64__reg_a0__c__native_first(uint64_t a)
{
    uint64_t v0 = (uint64_t)((int64_t)((int64_t)((uint64_t)a)) % (int64_t)((int64_t)((uint64_t)a)));
    int v1 = (((uint64_t)((uint64_t)a) == (uint64_t)(UINT64_C(0x8000000000000000)))) ? 1 : 0;
    int v2 = (((uint64_t)((uint64_t)a) == (uint64_t)(UINT64_C(0xffffffffffffffff)))) ? 1 : 0;
    int v3 = (((v2) && (v1))) ? 1 : 0;
    uint64_t v4 = ((v3) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)(v0));
    int v5 = (((uint64_t)((uint64_t)a) == (uint64_t)(UINT64_C(0x0)))) ? 1 : 0;
    uint64_t v6 = ((v5) ? (uint64_t)((uint64_t)a) : (uint64_t)(v4));
    return (uint64_t)(v6);
}
