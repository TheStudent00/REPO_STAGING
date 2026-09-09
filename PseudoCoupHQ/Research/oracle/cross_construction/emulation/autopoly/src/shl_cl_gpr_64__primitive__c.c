/* probe 684 -- binary << */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} << (int32_t){0})
emu_shl_cl_gpr_64__primitive__c(int64_t a, int32_t b)
{
    return a << b;
}
