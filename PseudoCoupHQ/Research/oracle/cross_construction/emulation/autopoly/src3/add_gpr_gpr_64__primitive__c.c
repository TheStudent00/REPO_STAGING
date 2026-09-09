/* probe 133 -- binary + */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} + (int64_t){0})
emu_add_gpr_gpr_64__primitive__c(bool a, int64_t b)
{
    return a + b;
}
