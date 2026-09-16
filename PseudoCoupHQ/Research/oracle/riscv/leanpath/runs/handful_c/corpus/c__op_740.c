/* probe 740 -- binary >> */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} >> (uint64_t){0})
op_740(double a, uint64_t b)
{
    return a >> b;
}
