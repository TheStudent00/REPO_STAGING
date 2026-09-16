/* probe 528 -- binary != */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} != (int32_t){0})
op_528(bool a, int32_t b)
{
    return a != b;
}
