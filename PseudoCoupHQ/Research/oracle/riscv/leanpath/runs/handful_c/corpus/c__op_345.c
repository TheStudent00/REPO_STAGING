/* probe 345 -- binary && */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} && (float){0})
op_345(double a, float b)
{
    return a && b;
}
