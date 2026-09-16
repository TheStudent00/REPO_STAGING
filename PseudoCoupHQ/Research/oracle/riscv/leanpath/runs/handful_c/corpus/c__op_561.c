/* probe 561 -- binary > */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} > (float){0})
op_561(double a, float b)
{
    return a > b;
}
