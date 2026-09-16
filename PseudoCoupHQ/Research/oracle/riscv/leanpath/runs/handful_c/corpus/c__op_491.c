/* probe 491 -- binary == */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} == (bool){0})
op_491(double a, bool b)
{
    return a == b;
}
