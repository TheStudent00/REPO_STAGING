/* probe 744 -- binary >> */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} >> (int32_t){0})
emu_shr_cl_gpr_32__primitive__c(bool a, int32_t b)
{
    return a >> b;
}
