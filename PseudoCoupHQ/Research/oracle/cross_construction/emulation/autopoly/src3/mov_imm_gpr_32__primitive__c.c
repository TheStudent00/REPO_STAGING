/* probe 49 -- unary sizeof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(sizeof (int64_t){0})
emu_mov_imm_gpr_32__primitive__c(int64_t a)
{
    return sizeof a;
}
