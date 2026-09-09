/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of control__E00319__c_regen_28697.  The term's layer-5 text, LITERAL:
   If(Extract(7, 0, v0) == Extract(7, 0, v1), 1, 0) */
#include <stdint.h>

uint8_t
emu_control__E00319__c_regen_28697(uint8_t a, uint8_t b)
{
    return (uint8_t)(((((uint32_t)((uint32_t)a) == (uint32_t)((uint32_t)b))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0))));
}
