/* task o13 emulation WITH THE MODE -- rendered by mode.py ModeRendererC from the layer-4 term
   of c__E01552__go_regen_341, and from the guard the reference read off the x unit's own body.
   The term's layer-5 text, LITERAL:
   ~(~LShR(v0, Concat(0, Extract(5, 0, v1))) | ~(18446744073709551615*If(Or(Not(Extract(15, 7, v1) == 0), ULE(64, Extract(6, 0, v1))), 0, 1))) */
#include <stdint.h>

uint64_t
emu_c__E01552__go_regen_341(uint64_t a, uint16_t b)
{
    return (uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)((uint64_t)a) >> (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x3f))))))))) | (uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)(((((((uint32_t)(UINT32_C(0x40)) <= (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x7f))))) || ((!(((uint32_t)(((uint32_t)((uint32_t)b >> 7) & UINT32_C(0x1ff))) == (uint32_t)(UINT32_C(0x0)))))))) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)(UINT64_C(0x1)))) * (uint64_t)(UINT64_C(0xffffffffffffffff))))))))));
}
