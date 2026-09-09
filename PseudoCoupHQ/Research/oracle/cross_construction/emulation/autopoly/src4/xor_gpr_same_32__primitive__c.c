/* probe 251 -- binary % */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} % (bool){0})
emu_xor_gpr_same_32__primitive__c(int32_t a, bool b)
{
    return a % b;
}
