/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of seto_gpr_one_8__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(63, 8, v2), If(Extract(7, 7, Concat(Extract(7, 7, v0), Extract(7, 0, v0)) + Concat(Extract(7, 7, v1), Extract(7, 0, v1))) == Extract(8, 8, Concat(Extract(7, 7, v0), Extract(7, 0, v0)) + Concat(Extract(7, 7, v1), Extract(7, 0, v1))), 0, 1)) */
#include <stdint.h>

uint64_t
emu_seto_gpr_one_8__reg_rdi__c(uint8_t a, uint8_t b, uint64_t c)
{
    return (uint64_t)((uint64_t)(((uint64_t)(((uint64_t)((uint64_t)c >> 8) & UINT64_C(0xffffffffffffff))) << 8) | (uint64_t)(((((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(((uint32_t)(((uint32_t)((uint32_t)b >> 7) & UINT32_C(0x1))) << 8) | (uint32_t)((uint32_t)b)) & UINT32_C(0x1ff))) + (uint32_t)(((uint32_t)(((uint32_t)(((uint32_t)((uint32_t)a >> 7) & UINT32_C(0x1))) << 8) | (uint32_t)((uint32_t)a)) & UINT32_C(0x1ff)))) & UINT32_C(0x1ff))) >> 7) & UINT32_C(0x1))) == (uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(((uint32_t)(((uint32_t)((uint32_t)b >> 7) & UINT32_C(0x1))) << 8) | (uint32_t)((uint32_t)b)) & UINT32_C(0x1ff))) + (uint32_t)(((uint32_t)(((uint32_t)(((uint32_t)((uint32_t)a >> 7) & UINT32_C(0x1))) << 8) | (uint32_t)((uint32_t)a)) & UINT32_C(0x1ff)))) & UINT32_C(0x1ff))) >> 8) & UINT32_C(0x1))))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1))))));
}
