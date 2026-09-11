/* probe 246 -- binary % */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} % (int32_t){0})
emu_idiv_gpr_one_32__primitive__c(int32_t a, int32_t b)
{
    return a % b;
}
