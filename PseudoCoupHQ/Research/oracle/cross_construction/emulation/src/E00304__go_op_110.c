/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E00304__go_op_110.  The term's layer-5 text, LITERAL:
   Extract(31, 0, bvudiv_i(Concat(0, v0), Concat(0, v1))) */
#include <stdint.h>

uint32_t
emu_E00304__go_op_110(uint64_t a, uint64_t b)
{
    return (uint32_t)((uint32_t)((unsigned __int128)((unsigned __int128)((unsigned __int128)((unsigned __int128)(((unsigned __int128)(UINT64_C(0x0)) << 64) | (unsigned __int128)((uint64_t)a))) / (unsigned __int128)((unsigned __int128)(((unsigned __int128)(UINT64_C(0x0)) << 64) | (unsigned __int128)((uint64_t)b))))) >> 0));
}
