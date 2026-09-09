/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of add_gpr_same_8__flags__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(7, 0, v0), Extract(7, 0, v0)) */
#include <stdint.h>

uint16_t
emu_add_gpr_same_8__flags__c(uint8_t a)
{
    return (uint16_t)(((uint32_t)(((uint32_t)((uint32_t)a) << 8) | (uint32_t)((uint32_t)a)) & UINT32_C(0xffff)));
}
