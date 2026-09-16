/* probe 601 -- binary >= */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} >= (int64_t){0})
op_601(bool a, int64_t b)
{
    return a >= b;
}
