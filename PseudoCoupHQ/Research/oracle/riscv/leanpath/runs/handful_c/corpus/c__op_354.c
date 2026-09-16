/* probe 354 -- binary | */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} | (int32_t){0})
op_354(int32_t a, int32_t b)
{
    return a | b;
}
