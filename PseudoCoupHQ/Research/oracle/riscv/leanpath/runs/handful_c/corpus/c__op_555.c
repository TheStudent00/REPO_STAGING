/* probe 555 -- binary > */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0} > (float){0})
op_555(float a, float b)
{
    return a > b;
}
