/* probe 741 -- binary >> */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} >> (float){0})
op_741(double a, float b)
{
    return a >> b;
}
