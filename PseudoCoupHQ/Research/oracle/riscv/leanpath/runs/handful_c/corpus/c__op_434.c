/* probe 434 -- binary & */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} & (uint64_t){0})
op_434(int64_t a, uint64_t b)
{
    return a & b;
}
