/* probe 365 -- binary | */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} | (bool){0})
op_365(int64_t a, bool b)
{
    return a | b;
}
