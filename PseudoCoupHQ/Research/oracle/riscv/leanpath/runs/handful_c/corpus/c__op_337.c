/* probe 337 -- binary && */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0} && (int64_t){0})
op_337(float a, int64_t b)
{
    return a && b;
}
