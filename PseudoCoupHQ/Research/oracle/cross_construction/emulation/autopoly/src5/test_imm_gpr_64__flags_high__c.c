/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of test_imm_gpr_64__flags_high__c.  The term's layer-5 text, LITERAL:
   ~(~v0 | ~v1) */
#include <stdint.h>

uint64_t
emu_test_imm_gpr_64__flags_high__c(uint64_t a, uint64_t b)
{
    return (uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)((uint64_t)(~(uint64_t)((uint64_t)a))) | (uint64_t)((uint64_t)(~(uint64_t)((uint64_t)b)))))));
}
