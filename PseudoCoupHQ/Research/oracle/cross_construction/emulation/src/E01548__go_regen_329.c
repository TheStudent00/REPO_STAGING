/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01548__go_regen_329.  The term's layer-5 text, LITERAL:
   Extract(7, 0, v1) >> Concat(0, Extract(4, 0, v0) | ~(31*If(Or(Not(Extract(63, 4, v0) == 0), ULE(8, Extract(3, 0, v0))), 0, 1))) */
#include <stdint.h>

uint8_t
emu_E01548__go_regen_329(uint8_t a, uint64_t b, uint64_t c)
{
    return (uint8_t)((((uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((((((uint32_t)(UINT32_C(0x8)) <= (uint32_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0xf))))) || ((!(((uint64_t)(((uint64_t)((uint64_t)b >> 4) & UINT64_C(0xfffffffffffffff))) == (uint64_t)(UINT64_C(0x0)))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1)))) * (uint32_t)(UINT32_C(0x1f))) & UINT32_C(0x1f)))) & UINT32_C(0x1f))) | (uint32_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0x1f)))) & UINT32_C(0xff))) < (uint32_t)8) ? ((uint32_t)(((int32_t)((uint32_t)((uint32_t)a) << 24) >> 24) >> (unsigned)(uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((((((uint32_t)(UINT32_C(0x8)) <= (uint32_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0xf))))) || ((!(((uint64_t)(((uint64_t)((uint64_t)b >> 4) & UINT64_C(0xfffffffffffffff))) == (uint64_t)(UINT64_C(0x0)))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1)))) * (uint32_t)(UINT32_C(0x1f))) & UINT32_C(0x1f)))) & UINT32_C(0x1f))) | (uint32_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0x1f)))) & UINT32_C(0xff)))) & UINT32_C(0xff)) : ((((int32_t)((uint32_t)((uint32_t)a) << 24) >> 24) < 0) ? UINT32_C(0xff) : (uint32_t)0)));
}
