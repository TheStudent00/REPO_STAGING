/* probe 542 -- binary > */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} > (uint64_t){0})
op_542(int64_t a, uint64_t b)
{
    return a > b;
}
