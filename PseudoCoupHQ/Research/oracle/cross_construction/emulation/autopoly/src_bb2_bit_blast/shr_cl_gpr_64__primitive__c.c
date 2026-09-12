/* probe 727 -- binary >> */
#include <stdint.h>
#include <stdbool.h>

__typeof__((uint64_t){0} >> (int64_t){0})
emu_shr_cl_gpr_64__primitive__c(uint64_t a, int64_t b)
{
    return a >> b;
}
