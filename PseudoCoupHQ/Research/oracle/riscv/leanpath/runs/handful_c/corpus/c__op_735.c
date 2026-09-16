/* probe 735 -- binary >> */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0} >> (float){0})
op_735(float a, float b)
{
    return a >> b;
}
