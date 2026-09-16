/* probe 518 -- binary != */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0} != (uint64_t){0})
op_518(float a, uint64_t b)
{
    return a != b;
}
