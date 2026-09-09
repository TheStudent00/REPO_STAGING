/* probe 726 -- binary >> */
#include <stdint.h>
#include <stdbool.h>

__typeof__((uint64_t){0} >> (int32_t){0})
emu_shr_cl_gpr_64__primitive__c(uint64_t a, int32_t b)
{
    return a >> b;
}
