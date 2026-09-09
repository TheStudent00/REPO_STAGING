/* probe 253 -- binary % */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} % (int64_t){0})
emu_idiv_gpr_one_64__primitive__c(int64_t a, int64_t b)
{
    return a % b;
}
