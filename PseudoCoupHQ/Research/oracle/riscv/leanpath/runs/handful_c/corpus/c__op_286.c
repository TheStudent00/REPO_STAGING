/* probe 286 -- binary || */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} || (double){0})
op_286(int32_t a, double b)
{
    return a || b;
}
