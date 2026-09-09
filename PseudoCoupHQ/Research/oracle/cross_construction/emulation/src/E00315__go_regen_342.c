/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E00315__go_regen_342.  The term's layer-5 text, LITERAL:
   ~(~LShR(v0, Concat(0, Extract(5, 0, v1))) | ~(18446744073709551615*If(Or(Not(Extract(31, 7, v1) == 0), ULE(64, Extract(6, 0, v1))), 0, 1))) */
#include <stdint.h>

uint64_t
emu_E00315__go_regen_342(uint64_t a, uint32_t b)
{
    return (uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)((uint64_t)a) >> (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x3f))))))))) | (uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)(((((((uint32_t)(UINT32_C(0x40)) <= (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x7f))))) || ((!(((uint32_t)(((uint32_t)((uint32_t)b >> 7) & UINT32_C(0x1ffffff))) == (uint32_t)(UINT32_C(0x0)))))))) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)(UINT64_C(0x1)))) * (uint64_t)(UINT64_C(0xffffffffffffffff))))))))));
}
