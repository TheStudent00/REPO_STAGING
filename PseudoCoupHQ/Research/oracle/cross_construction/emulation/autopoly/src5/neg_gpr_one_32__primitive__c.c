/* probe 12 -- unary - */
#include <stdint.h>
#include <stdbool.h>

__typeof__(-(int32_t){0})
emu_neg_gpr_one_32__primitive__c(int32_t a)
{
    return -a;
}
