/* probe 633 -- binary <= */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} <= (float){0})
op_633(double a, float b)
{
    return a <= b;
}
