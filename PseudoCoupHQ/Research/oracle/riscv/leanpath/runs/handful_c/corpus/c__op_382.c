/* probe 382 -- binary | */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} | (double){0})
op_382(double a, double b)
{
    return a | b;
}
