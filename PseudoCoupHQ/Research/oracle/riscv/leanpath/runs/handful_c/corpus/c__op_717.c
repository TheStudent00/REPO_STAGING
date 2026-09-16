/* probe 717 -- binary >> */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} >> (float){0})
op_717(int32_t a, float b)
{
    return a >> b;
}
