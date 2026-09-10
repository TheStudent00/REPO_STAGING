/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of sltiu_gpr_gpr_imm_64__reg_a0__c.  The term's layer-5 text, LITERAL:
   If(Or(Extract(1, 0, v0) == 3, Not(Extract(63, 2, v0) == 0)), 0, 1) */
#include <stdint.h>

uint64_t
emu_sltiu_gpr_gpr_imm_64__reg_a0__c(uint64_t a)
{
    return (uint64_t)(((((((uint32_t)(((uint32_t)((uint64_t)a >> 0) & UINT32_C(0x3))) == (uint32_t)(UINT32_C(0x3)))) || ((!(((uint64_t)(((uint64_t)((uint64_t)a >> 2) & UINT64_C(0x3fffffffffffffff))) == (uint64_t)(UINT64_C(0x0)))))))) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)(UINT64_C(0x1))));
}
