/* probe 580 -- binary >= */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int64_t){0} >= (double){0})
op_580(int64_t a, double b)
{
    return a >= b;
}
