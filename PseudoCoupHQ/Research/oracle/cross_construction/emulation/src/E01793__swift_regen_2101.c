/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01793__swift_regen_2101.  The term's layer-5 text, LITERAL:
   If(Or(Not(Extract(7, 7, v0) == 0), ULE(64, Extract(6, 0, v0))), 0, LShR(v1, Concat(0, Extract(5, 0, v0)))) */
#include <stdint.h>

uint64_t
emu_E01793__swift_regen_2101(uint64_t a, uint8_t b)
{
    return (uint64_t)(((((((uint32_t)(UINT32_C(0x40)) <= (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x7f))))) || ((!(((uint32_t)(((uint32_t)((uint32_t)b >> 7) & UINT32_C(0x1))) == (uint32_t)(UINT32_C(0x0)))))))) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)((uint64_t)((uint64_t)((uint64_t)a) >> (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x3f)))))))));
}
