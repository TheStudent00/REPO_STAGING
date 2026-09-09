/* probe 47 -- unary -- */
#include <stdint.h>
#include <stdbool.h>

__typeof__(--(bool){0})
emu_xor_imm_gpr_8__primitive__c(bool a)
{
    return --a;
}
