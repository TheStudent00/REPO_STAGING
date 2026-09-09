/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01542__go_regen_296.  The term's layer-5 text, LITERAL:
   Extract(15, 0, v1) >> Concat(0, Extract(4, 0, v0) | ~(31*If(Or(Not(Extract(63, 5, v0) == 0), ULE(16, Extract(4, 0, v0))), 0, 1))) */
#include <stdint.h>

uint16_t
emu_E01542__go_regen_296(uint16_t a, uint64_t b, uint64_t c)
{
    return (uint16_t)((((uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((((((uint32_t)(UINT32_C(0x10)) <= (uint32_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x1f))))) || ((!(((uint64_t)(((uint64_t)((uint64_t)b >> 5) & UINT64_C(0x7ffffffffffffff))) == (uint64_t)(UINT64_C(0x0)))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1)))) * (uint32_t)(UINT32_C(0x1f))) & UINT32_C(0x1f)))) & UINT32_C(0x1f))) | (uint32_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0x1f)))) & UINT32_C(0xffff))) < (uint32_t)16) ? ((uint32_t)(((int32_t)((uint32_t)((uint32_t)a) << 16) >> 16) >> (unsigned)(uint32_t)(((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((((((uint32_t)(UINT32_C(0x10)) <= (uint32_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x1f))))) || ((!(((uint64_t)(((uint64_t)((uint64_t)b >> 5) & UINT64_C(0x7ffffffffffffff))) == (uint64_t)(UINT64_C(0x0)))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1)))) * (uint32_t)(UINT32_C(0x1f))) & UINT32_C(0x1f)))) & UINT32_C(0x1f))) | (uint32_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x1f)))) & UINT32_C(0x1f)))) & UINT32_C(0xffff)))) & UINT32_C(0xffff)) : ((((int32_t)((uint32_t)((uint32_t)a) << 16) >> 16) < 0) ? UINT32_C(0xffff) : (uint32_t)0)));
}
