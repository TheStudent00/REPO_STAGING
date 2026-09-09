/* probe 11 -- unary ~ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(~(bool){0})
emu_not_gpr_one_32__primitive__c(bool a)
{
    return ~a;
}
