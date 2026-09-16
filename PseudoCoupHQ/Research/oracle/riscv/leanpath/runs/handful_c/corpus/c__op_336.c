/* probe 336 -- binary && */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0} && (int32_t){0})
op_336(float a, int32_t b)
{
    return a && b;
}
