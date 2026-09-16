/* probe 630 -- binary <= */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} <= (int32_t){0})
op_630(double a, int32_t b)
{
    return a <= b;
}
