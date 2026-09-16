/* probe 309 -- binary || */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} || (float){0})
op_309(double a, float b)
{
    return a || b;
}
