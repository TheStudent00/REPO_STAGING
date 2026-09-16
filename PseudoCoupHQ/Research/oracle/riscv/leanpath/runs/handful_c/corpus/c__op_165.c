/* probe 165 -- binary - */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} - (float){0})
op_165(double a, float b)
{
    return a - b;
}
