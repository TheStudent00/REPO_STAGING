/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of sbb_imm_gpr_8__flags__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(7, 0, v0), Extract(7, 0, v1)) */
#include <stdint.h>

uint16_t
emu_sbb_imm_gpr_8__flags__c(uint8_t a, uint8_t b)
{
    return (uint16_t)(((uint32_t)(((uint32_t)((uint32_t)a) << 8) | (uint32_t)((uint32_t)b)) & UINT32_C(0xffff)));
}
