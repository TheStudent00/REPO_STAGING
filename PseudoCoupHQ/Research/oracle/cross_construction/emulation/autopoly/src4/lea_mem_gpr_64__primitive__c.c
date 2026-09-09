/* probe 43 -- unary -- */
#include <stdint.h>
#include <stdbool.h>

__typeof__(--(int64_t){0})
emu_lea_mem_gpr_64__primitive__c(int64_t a)
{
    return --a;
}
