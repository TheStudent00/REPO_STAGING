/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01611__swift_regen_322.  The term's layer-5 text, LITERAL:
   Concat(Extract(31, 16, v0), Extract(15, 0, bvudiv_i(Concat(0, Extract(15, 0, v0)), Concat(0, Extract(15, 0, v1))))) */
#include <stdint.h>

uint32_t
emu_E01611__swift_regen_322(uint32_t a, uint16_t b, uint64_t c)
{
    return (uint32_t)((uint32_t)(((uint32_t)(((uint32_t)((uint32_t)a >> 16) & UINT32_C(0xffff))) << 16) | (uint32_t)(((uint32_t)((uint32_t)((uint32_t)((uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)(((uint32_t)((uint32_t)a >> 0) & UINT32_C(0xffff))))) / (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)((uint32_t)b))))) >> 0) & UINT32_C(0xffff)))));
}
