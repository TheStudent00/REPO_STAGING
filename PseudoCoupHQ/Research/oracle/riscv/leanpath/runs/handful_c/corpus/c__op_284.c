/* probe 284 -- binary || */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} || (uint64_t){0})
op_284(int32_t a, uint64_t b)
{
    return a || b;
}
