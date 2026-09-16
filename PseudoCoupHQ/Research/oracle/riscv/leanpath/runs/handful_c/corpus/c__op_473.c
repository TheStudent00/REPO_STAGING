/* probe 473 -- binary == */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} == (bool){0})
op_473(int64_t a, bool b)
{
    return a == b;
}
