/* probe 295 -- binary || */
#include <stdint.h>
#include <stdbool.h>

__typeof__((uint64_t){0} || (int64_t){0})
op_295(uint64_t a, int64_t b)
{
    return a || b;
}
