/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of test_gpr_same_32__flags__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(31, 0, v0), 0) */
#include <stdint.h>

uint64_t
emu_test_gpr_same_32__flags__c(uint32_t a)
{
    return (uint64_t)((uint64_t)(((uint64_t)((uint32_t)a) << 32) | (uint64_t)(UINT32_C(0x0))));
}
