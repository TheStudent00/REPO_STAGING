/* probe 7 -- unary ~ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(~(int64_t){0})
emu_not_gpr_one_64__primitive__c(int64_t a)
{
    return ~a;
}
