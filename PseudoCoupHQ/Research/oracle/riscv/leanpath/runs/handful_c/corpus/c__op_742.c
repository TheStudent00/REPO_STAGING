/* probe 742 -- binary >> */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} >> (double){0})
op_742(double a, double b)
{
    return a >> b;
}
