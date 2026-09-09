/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of control__E00672__c_regen_20875.  The term's layer-5 text, LITERAL:
   Concat(0, ~(~(If(fpIsNaN(fpToFP(Extract(63, 0, v0))), 1, 0) | If(Or(Not(fpEQ(fpToFP(Extract(63, 0, v0)), +0.0)), fpIsNaN(fpToFP(Extract(63, 0, v0)))), 1, 0)) | If(Extract(15, 0, v1) == 0, 255, 254))) */
#include <stdint.h>

uint32_t
emu_control__E00672__c_regen_20875(uint16_t a, uint64_t b, uint64_t c, double d, double e)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((((d) != (d))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0)))) | (uint32_t)(((((((d) != (d))) || ((!(((d) == (0.0))))))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0))))) & UINT32_C(0xff)))) & UINT32_C(0xff))) | (uint32_t)(((((uint32_t)((uint32_t)a) == (uint32_t)(UINT32_C(0x0)))) ? (uint32_t)(UINT32_C(0xff)) : (uint32_t)(UINT32_C(0xfe))))) & UINT32_C(0xff)))) & UINT32_C(0xff)))));
}
