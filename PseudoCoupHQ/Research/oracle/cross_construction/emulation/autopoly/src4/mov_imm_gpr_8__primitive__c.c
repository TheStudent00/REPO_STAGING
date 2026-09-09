/* probe 41 -- unary ++ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(++(bool){0})
emu_mov_imm_gpr_8__primitive__c(bool a)
{
    return ++a;
}
