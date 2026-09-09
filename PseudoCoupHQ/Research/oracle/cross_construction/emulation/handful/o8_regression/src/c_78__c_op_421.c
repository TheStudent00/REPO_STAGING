/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of c_78__c_op_421.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 32, v0), Extract(31, 0, v0) ^ Extract(31, 0, v1)) */
#include <stdint.h>

uint64_t
emu_c_78__c_op_421(uint32_t a, uint64_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)((uint32_t)((uint64_t)b >> 32)) << 32) | (uint64_t)((uint32_t)((uint32_t)((uint32_t)a) ^ (uint32_t)((uint32_t)((uint64_t)b >> 0))))));
}
