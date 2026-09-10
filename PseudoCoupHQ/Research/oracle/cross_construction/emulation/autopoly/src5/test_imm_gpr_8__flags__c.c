/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of test_imm_gpr_8__flags__c.  The term's layer-5 text, LITERAL:
   Concat(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)), 0) */
#include <stdint.h>

uint16_t
emu_test_imm_gpr_8__flags__c(uint8_t a, uint8_t b)
{
    return (uint16_t)(((uint32_t)(((uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)((uint32_t)b)) & UINT32_C(0xff))) | (uint32_t)(((uint32_t)(~(uint32_t)((uint32_t)a)) & UINT32_C(0xff)))) & UINT32_C(0xff)))) & UINT32_C(0xff))) << 8) | (uint32_t)(UINT32_C(0x0))) & UINT32_C(0xffff)));
}
