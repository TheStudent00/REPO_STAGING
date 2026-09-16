/* probe 240 -- binary / */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} / (int32_t){0})
op_240(bool a, int32_t b)
{
    return a / b;
}
