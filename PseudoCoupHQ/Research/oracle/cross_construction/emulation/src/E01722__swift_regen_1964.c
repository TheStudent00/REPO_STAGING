/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01722__swift_regen_1964.  The term's layer-5 text, LITERAL:
   If(Or(Not(Extract(6, 6, v0) == 0), Not(Extract(63, 8, v0) == 0), ULE(128, Extract(7, 0, v0))), 0, v1 << Concat(0, Extract(5, 0, v0))) */
#include <stdint.h>

uint64_t
emu_E01722__swift_regen_1964(uint64_t a, uint64_t b, uint64_t c)
{
    return (uint64_t)(((((((uint32_t)(UINT32_C(0x80)) <= (uint32_t)(((uint32_t)((uint64_t)c >> 0) & UINT32_C(0xff))))) || ((!(((uint32_t)(((uint32_t)((uint64_t)c >> 6) & UINT32_C(0x1))) == (uint32_t)(UINT32_C(0x0)))))) || ((!(((uint64_t)(((uint64_t)((uint64_t)c >> 8) & UINT64_C(0xffffffffffffff))) == (uint64_t)(UINT64_C(0x0)))))))) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)((uint64_t)((uint64_t)((uint64_t)a) << (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((uint32_t)((uint64_t)c >> 0) & UINT32_C(0x3f)))))))));
}
