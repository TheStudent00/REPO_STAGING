/* probe 429 -- binary & */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} & (float){0})
op_429(int32_t a, float b)
{
    return a & b;
}
