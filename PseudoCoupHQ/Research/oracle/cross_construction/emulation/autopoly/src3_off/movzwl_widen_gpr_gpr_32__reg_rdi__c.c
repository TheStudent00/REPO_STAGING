/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of movzwl_widen_gpr_gpr_32__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(15, 0, v0)) */
#include <stdint.h>

uint64_t
emu_movzwl_widen_gpr_gpr_32__reg_rdi__c(uint16_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 16) | (uint64_t)((uint32_t)a)));
}
