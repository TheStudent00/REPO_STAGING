/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of control__E00638__c_regen_19988.  The term's layer-5 text, LITERAL:
   Concat(0, ~(If(Extract(15, 0, v0) == 0, 255, 254) | If(v1 | v2 == 0, 255, 254))) */
#include <stdint.h>

uint32_t
emu_control__E00638__c_regen_19988(uint64_t a, uint64_t b, uint16_t c, uint64_t d)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((((uint64_t)((uint64_t)((uint64_t)((uint64_t)a) | (uint64_t)((uint64_t)b))) == (uint64_t)(UINT64_C(0x0)))) ? (uint32_t)(UINT32_C(0xff)) : (uint32_t)(UINT32_C(0xfe)))) | (uint32_t)(((((uint32_t)((uint32_t)c) == (uint32_t)(UINT32_C(0x0)))) ? (uint32_t)(UINT32_C(0xff)) : (uint32_t)(UINT32_C(0xfe))))) & UINT32_C(0xff)))) & UINT32_C(0xff)))));
}
