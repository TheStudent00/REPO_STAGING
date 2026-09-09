/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01752__swift_regen_2026.  The term's layer-5 text, LITERAL:
   v1 >> Concat(0, If(Or(Not(Extract(15, 6, v0) == 0), Extract(5, 0, v0) == 63), 63, Extract(5, 0, v0))) */
#include <stdint.h>

uint64_t
emu_E01752__swift_regen_2026(uint64_t a, uint16_t b)
{
    return (uint64_t)((uint64_t)((int64_t)((uint64_t)a) >> (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((((((uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x3f))) == (uint32_t)(UINT32_C(0x3f)))) || ((!(((uint32_t)(((uint32_t)((uint32_t)b >> 6) & UINT32_C(0x3ff))) == (uint32_t)(UINT32_C(0x0)))))))) ? (uint32_t)(UINT32_C(0x3f)) : (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x3f)))))))));
}
