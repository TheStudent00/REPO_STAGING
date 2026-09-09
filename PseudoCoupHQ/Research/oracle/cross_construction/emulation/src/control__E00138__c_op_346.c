/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of control__E00138__c_op_346.  The term's layer-5 text, LITERAL:
   ~(4294967294 | If(And(fpEQ(fpToFP(Extract(63, 0, v0)), +0.0), Not(fpIsNaN(fpToFP(Extract(63, 0, v0))))), 4294967295, 0) | If(And(fpEQ(fpToFP(Extract(63, 0, v1)), +0.0), Not(fpIsNaN(fpToFP(Extract(63, 0, v1))))), 4294967295, 0)) */
#include <stdint.h>

uint32_t
emu_control__E00138__c_op_346(double a, double b, double c)
{
    return (uint32_t)((uint32_t)(~(uint32_t)((uint32_t)((uint32_t)(((((((a) == (0.0))) && ((!(((a) != (a))))))) ? (uint32_t)(UINT32_C(0xffffffff)) : (uint32_t)(UINT32_C(0x0)))) | (uint32_t)(((((((b) == (0.0))) && ((!(((b) != (b))))))) ? (uint32_t)(UINT32_C(0xffffffff)) : (uint32_t)(UINT32_C(0x0)))) | (uint32_t)(UINT32_C(0xfffffffe))))));
}
