/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01559__go_regen_363.  The term's layer-5 text, LITERAL:
   ~(~LShR(Extract(31, 0, v0), Concat(0, Extract(4, 0, v1))) | ~(4294967295*If(Or(Not(Extract(15, 6, v1) == 0), ULE(32, Extract(5, 0, v1))), 0, 1))) */
#include <stdint.h>

uint32_t
emu_E01559__go_regen_363(uint32_t a, uint16_t b)
{
    return (uint32_t)((uint32_t)(~(uint32_t)((uint32_t)((uint32_t)((uint32_t)(~(uint32_t)((uint32_t)((uint32_t)((uint32_t)a) >> (unsigned)(uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f))))))))) | (uint32_t)((uint32_t)(~(uint32_t)((uint32_t)((uint32_t)(((((((uint32_t)(UINT32_C(0x20)) <= (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x3f))))) || ((!(((uint32_t)(((uint32_t)((uint32_t)b >> 6) & UINT32_C(0x3ff))) == (uint32_t)(UINT32_C(0x0)))))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1)))) * (uint32_t)(UINT32_C(0xffffffff))))))))));
}
