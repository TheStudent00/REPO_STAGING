/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of control__E00959__c_regen_39327.  The term's layer-5 text, LITERAL:
   If(Extract(15, 0, v0) <= Extract(15, 0, v1), 1, 0) */
#include <stdint.h>

uint8_t
emu_control__E00959__c_regen_39327(uint16_t a, uint16_t b)
{
    return (uint8_t)((((((int32_t)((uint32_t)((uint32_t)b) << 16) >> 16) <= ((int32_t)((uint32_t)((uint32_t)a) << 16) >> 16))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0))));
}
