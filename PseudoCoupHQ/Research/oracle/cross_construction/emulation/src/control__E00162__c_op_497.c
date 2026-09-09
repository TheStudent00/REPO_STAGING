/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of control__E00162__c_op_497.  The term's layer-5 text, LITERAL:
   Concat(0, 1 ^ Extract(7, 0, v0) ^ Extract(7, 0, v1)) */
#include <stdint.h>

uint32_t
emu_control__E00162__c_op_497(uint8_t a, uint8_t b)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)(((uint32_t)((uint32_t)((uint32_t)a) ^ (uint32_t)((uint32_t)b) ^ (uint32_t)(UINT32_C(0x1))) & UINT32_C(0xff)))));
}
