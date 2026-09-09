/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of control__E00139__c_op_347.  The term's layer-5 text, LITERAL:
   Concat(0, ~(~Extract(7, 0, v1) | ~(If(fpIsNaN(fpToFP(Extract(63, 0, v0))), 1, 0) | If(Or(fpIsNaN(fpToFP(Extract(63, 0, v0))), Not(fpEQ(fpToFP(Extract(63, 0, v0)), +0.0))), 1, 0)))) */
#include <stdint.h>

uint32_t
emu_control__E00139__c_op_347(uint8_t a, uint64_t b, double c, double d)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((((c) != (c))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0)))) | (uint32_t)(((((((c) != (c))) || ((!(((c) == (0.0))))))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0))))) & UINT32_C(0xff)))) & UINT32_C(0xff))) | (uint32_t)(((uint32_t)(~(uint32_t)((uint32_t)a)) & UINT32_C(0xff)))) & UINT32_C(0xff)))) & UINT32_C(0xff)))));
}
