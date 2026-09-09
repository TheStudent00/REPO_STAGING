/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of c_71__c_op_169.  The term's layer-5 text, LITERAL:
   v0*18446744073709551615 + Concat(0, Extract(31, 0, v1)) */
#include <stdint.h>

uint64_t
emu_c_71__c_op_169(uint32_t a, uint64_t b)
{
    return (uint64_t)((uint64_t)((uint64_t)((uint64_t)((uint64_t)((uint64_t)b) * (uint64_t)(UINT64_C(0xffffffffffffffff)))) + (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)a)))));
}
