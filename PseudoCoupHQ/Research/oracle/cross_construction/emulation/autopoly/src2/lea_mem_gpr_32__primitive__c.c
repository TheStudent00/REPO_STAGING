/* probe 42 -- unary -- */
#include <stdint.h>
#include <stdbool.h>

__typeof__(--(int32_t){0})
emu_lea_mem_gpr_32__primitive__c(int32_t a)
{
    return --a;
}
