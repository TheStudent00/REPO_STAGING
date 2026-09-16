/* probe 585 -- binary >= */
#include <stdint.h>
#include <stdbool.h>

__typeof__((uint64_t){0} >= (float){0})
op_585(uint64_t a, float b)
{
    return a >= b;
}
