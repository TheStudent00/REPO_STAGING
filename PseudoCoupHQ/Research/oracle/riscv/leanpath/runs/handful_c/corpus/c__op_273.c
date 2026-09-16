/* probe 273 -- binary % */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} % (float){0})
op_273(double a, float b)
{
    return a % b;
}
