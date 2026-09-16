/* probe 588 -- binary >= */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0} >= (int32_t){0})
op_588(float a, int32_t b)
{
    return a >= b;
}
