/* probe 282 -- binary || */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} || (int32_t){0})
op_282(int32_t a, int32_t b)
{
    return a || b;
}
