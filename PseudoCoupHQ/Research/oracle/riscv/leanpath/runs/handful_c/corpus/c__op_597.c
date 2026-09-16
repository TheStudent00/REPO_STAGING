/* probe 597 -- binary >= */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} >= (float){0})
op_597(double a, float b)
{
    return a >= b;
}
