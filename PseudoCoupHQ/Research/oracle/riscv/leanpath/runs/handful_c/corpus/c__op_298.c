/* probe 298 -- binary || */
#include <stdint.h>
#include <stdbool.h>

__typeof__((uint64_t){0} || (double){0})
op_298(uint64_t a, double b)
{
    return a || b;
}
