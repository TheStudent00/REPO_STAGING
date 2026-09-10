/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of imul_gpr_gpr_16__flags__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(15, 0, v0), Extract(15, 0, v1)) */
#include <stdint.h>

uint32_t
emu_imul_gpr_gpr_16__flags__c(uint16_t a, uint16_t b)
{
    return (uint32_t)((uint32_t)(((uint32_t)((uint32_t)a) << 16) | (uint32_t)((uint32_t)b)));
}
