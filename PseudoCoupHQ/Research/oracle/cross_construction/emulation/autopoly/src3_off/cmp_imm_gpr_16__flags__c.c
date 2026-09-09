/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of cmp_imm_gpr_16__flags__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(15, 0, v0), 3) */
#include <stdint.h>

uint32_t
emu_cmp_imm_gpr_16__flags__c(uint16_t a)
{
    return (uint32_t)((uint32_t)(((uint32_t)((uint32_t)a) << 16) | (uint32_t)(UINT32_C(0x3))));
}
