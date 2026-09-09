/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of or_imm_gpr_8__flags__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(7, 2, v0), 768) */
#include <stdint.h>

uint16_t
emu_or_imm_gpr_8__flags__c(uint8_t a)
{
    return (uint16_t)(((uint32_t)(((uint32_t)(((uint32_t)((uint32_t)a >> 2) & UINT32_C(0x3f))) << 10) | (uint32_t)(UINT32_C(0x300))) & UINT32_C(0xffff)));
}
