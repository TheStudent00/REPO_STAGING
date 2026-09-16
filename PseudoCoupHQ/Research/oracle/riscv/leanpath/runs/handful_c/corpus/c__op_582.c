/* probe 582 -- binary >= */
#include <stdint.h>
#include <stdbool.h>

__typeof__((uint64_t){0} >= (int32_t){0})
op_582(uint64_t a, int32_t b)
{
    return a >= b;
}
