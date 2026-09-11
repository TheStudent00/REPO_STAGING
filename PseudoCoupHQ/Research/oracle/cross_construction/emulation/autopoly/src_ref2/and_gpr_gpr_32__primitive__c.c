/* probe 426 -- binary & */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} & (int32_t){0})
emu_and_gpr_gpr_32__primitive__c(int32_t a, int32_t b)
{
    return a & b;
}
