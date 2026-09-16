/* probe 4 -- unary ! */
#include <stdint.h>
#include <stdbool.h>

__typeof__(!(double){0})
op_4(double a)
{
    return !a;
}
