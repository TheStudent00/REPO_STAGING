/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01725__swift_regen_1969.  The term's layer-5 text, LITERAL:
   If(And(0 <= Extract(7, 0, v0), Extract(6, 6, v0) == 0), v1 << Concat(0, Extract(5, 0, v0)), 0) */
#include <stdint.h>

uint64_t
emu_E01725__swift_regen_1969(uint64_t a, uint64_t b, uint8_t c)
{
    return (uint64_t)(((((((uint32_t)(((uint32_t)((uint32_t)c >> 6) & UINT32_C(0x1))) == (uint32_t)(UINT32_C(0x0)))) && ((((int32_t)((uint32_t)(UINT32_C(0x0)) << 24) >> 24) <= ((int32_t)((uint32_t)((uint32_t)c) << 24) >> 24))))) ? (uint64_t)((uint64_t)((uint64_t)((uint64_t)a) << (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((uint32_t)((uint32_t)c >> 0) & UINT32_C(0x3f))))))) : (uint64_t)(UINT64_C(0x0))));
}
