/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E00311__go_regen_309.  The term's layer-5 text, LITERAL:
   Extract(31, 0, v1) >> Concat(0, Extract(4, 0, v0) | ~(31*If(Or(Not(Extract(31, 6, v0) == 0), ULE(32, Extract(5, 0, v0))), 0, 1))) */
#include <stdint.h>

uint32_t
emu_E00311__go_regen_309(uint32_t a, uint32_t b, uint64_t c)
{
    return (uint32_t)((((uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((((((uint32_t)(UINT32_C(0x20)) <= (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x3f))))) || ((!(((uint32_t)(((uint32_t)((uint32_t)b >> 6) & UINT32_C(0x3ffffff))) == (uint32_t)(UINT32_C(0x0)))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1)))) * (uint32_t)(UINT32_C(0x1f))) & UINT32_C(0x1f)))) & UINT32_C(0x1f))) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0x1f))))) < (uint32_t)32) ? (uint32_t)((int32_t)((uint32_t)a) >> (unsigned)(uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((((((uint32_t)(UINT32_C(0x20)) <= (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x3f))))) || ((!(((uint32_t)(((uint32_t)((uint32_t)b >> 6) & UINT32_C(0x3ffffff))) == (uint32_t)(UINT32_C(0x0)))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1)))) * (uint32_t)(UINT32_C(0x1f))) & UINT32_C(0x1f)))) & UINT32_C(0x1f))) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0x1f)))))) : (((int32_t)((uint32_t)a) < 0) ? UINT32_C(0xffffffff) : (uint32_t)0)));
}
