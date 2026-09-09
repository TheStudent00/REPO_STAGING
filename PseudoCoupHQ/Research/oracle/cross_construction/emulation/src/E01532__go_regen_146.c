/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E01532__go_regen_146.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(15, 0, bvudiv_i(Concat(0, Extract(7, 0, v0)), Concat(0, Extract(7, 0, v1))))) */
#include <stdint.h>

uint32_t
emu_E01532__go_regen_146(uint8_t a, uint8_t b)
{
    return (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 16) | (uint32_t)(((uint32_t)((uint32_t)((uint32_t)((uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)((uint32_t)a))) / (uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 8) | (uint32_t)((uint32_t)b))))) >> 0) & UINT32_C(0xffff)))));
}
