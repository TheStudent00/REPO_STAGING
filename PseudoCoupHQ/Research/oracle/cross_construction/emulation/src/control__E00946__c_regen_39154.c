/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of control__E00946__c_regen_39154.  The term's layer-5 text, LITERAL:
   Concat(0, If(v0 >> 63 <= v1, 1, 0)) */
#include <stdint.h>

uint32_t
emu_control__E00946__c_regen_39154(uint64_t a, uint64_t b, uint64_t c)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)(((((int64_t)((uint64_t)((int64_t)((uint64_t)c) >> (unsigned)(uint64_t)(UINT64_C(0x3f)))) <= (int64_t)((uint64_t)b))) ? (uint32_t)(UINT32_C(0x1)) : (uint32_t)(UINT32_C(0x0))))));
}
