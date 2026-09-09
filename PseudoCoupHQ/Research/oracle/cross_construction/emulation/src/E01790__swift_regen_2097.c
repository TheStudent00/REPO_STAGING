/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01790__swift_regen_2097.  The term's layer-5 text, LITERAL:
   If(And(v1 == 0, Not(Or(Not(Extract(63, 7, v0) == 0), ULE(64, Extract(6, 0, v0))))), LShR(v2, Concat(0, Extract(5, 0, v0))), 0) */
#include <stdint.h>

uint64_t
emu_E01790__swift_regen_2097(uint64_t a, uint64_t b, uint64_t c)
{
    return (uint64_t)(((((((uint64_t)((uint64_t)c) == (uint64_t)(UINT64_C(0x0)))) && ((!(((((uint32_t)(UINT32_C(0x40)) <= (uint32_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x7f))))) || ((!(((uint64_t)(((uint64_t)((uint64_t)b >> 7) & UINT64_C(0x1ffffffffffffff))) == (uint64_t)(UINT64_C(0x0)))))))))))) ? (uint64_t)((uint64_t)((uint64_t)((uint64_t)a) >> (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x3f))))))) : (uint64_t)(UINT64_C(0x0))));
}
