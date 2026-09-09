/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of c_79__c_op_47.  The term's layer-5 text, LITERAL:
   Concat(Extract(7, 1, v0), ~Extract(0, 0, v0)) */
#include <stdint.h>

uint8_t
emu_c_79__c_op_47(uint8_t a)
{
    return (uint8_t)(((uint32_t)(((uint32_t)(((uint32_t)((uint32_t)a >> 1) & UINT32_C(0x7f))) << 1) | (uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)a >> 0) & UINT32_C(0x1)))) & UINT32_C(0x1)))) & UINT32_C(0xff)));
}
