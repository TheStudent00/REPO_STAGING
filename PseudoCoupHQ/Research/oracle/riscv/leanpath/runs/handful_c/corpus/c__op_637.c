/* probe 637 -- binary <= */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} <= (int64_t){0})
op_637(bool a, int64_t b)
{
    return a <= b;
}
