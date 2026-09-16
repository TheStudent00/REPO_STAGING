/* probe 594 -- binary >= */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} >= (int32_t){0})
op_594(double a, int32_t b)
{
    return a >= b;
}
