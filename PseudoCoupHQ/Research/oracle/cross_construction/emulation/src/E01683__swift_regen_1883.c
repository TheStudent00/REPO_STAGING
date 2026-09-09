/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01683__swift_regen_1883.  The term's layer-5 text, LITERAL:
   If(Or(Not(Extract(31, 7, v0) == 0), ULE(64, Extract(6, 0, v0))), 0, v1 << Concat(0, Extract(5, 0, v0))) */
#include <stdint.h>

uint64_t
emu_E01683__swift_regen_1883(uint64_t a, uint32_t b)
{
    return (uint64_t)(((((((uint32_t)(UINT32_C(0x40)) <= (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x7f))))) || ((!(((uint32_t)(((uint32_t)((uint32_t)b >> 7) & UINT32_C(0x1ffffff))) == (uint32_t)(UINT32_C(0x0)))))))) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)((uint64_t)((uint64_t)((uint64_t)a) << (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x3f)))))))));
}
