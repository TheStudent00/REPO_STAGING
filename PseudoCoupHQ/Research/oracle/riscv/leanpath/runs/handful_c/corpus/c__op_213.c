/* probe 213 -- binary / */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} / (float){0})
op_213(int32_t a, float b)
{
    return a / b;
}
