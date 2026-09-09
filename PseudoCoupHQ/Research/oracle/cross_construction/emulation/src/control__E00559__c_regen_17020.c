/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of control__E00559__c_regen_17020.  The term's layer-5 text, LITERAL:
   Concat(0, If(Extract(7, 0, v0) == 0, 0, 1) | If(Extract(15, 0, v1) == 0, 0, 1)) */
#include <stdint.h>

uint32_t
emu_control__E00559__c_regen_17020(uint8_t a, uint16_t b, uint64_t c)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)(((uint32_t)((uint32_t)(((((uint32_t)((uint32_t)b) == (uint32_t)(UINT32_C(0x0)))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1)))) | (uint32_t)(((((uint32_t)((uint32_t)a) == (uint32_t)(UINT32_C(0x0)))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1))))) & UINT32_C(0xff)))));
}
