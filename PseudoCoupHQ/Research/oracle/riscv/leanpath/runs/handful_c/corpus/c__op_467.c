/* probe 467 -- binary == */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} == (bool){0})
op_467(int32_t a, bool b)
{
    return a == b;
}
