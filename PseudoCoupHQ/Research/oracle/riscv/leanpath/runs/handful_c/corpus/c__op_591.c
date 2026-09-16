/* probe 591 -- binary >= */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0} >= (float){0})
op_591(float a, float b)
{
    return a >= b;
}
