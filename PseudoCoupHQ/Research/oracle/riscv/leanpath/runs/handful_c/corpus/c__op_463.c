/* probe 463 -- binary == */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} == (int64_t){0})
op_463(int32_t a, int64_t b)
{
    return a == b;
}
